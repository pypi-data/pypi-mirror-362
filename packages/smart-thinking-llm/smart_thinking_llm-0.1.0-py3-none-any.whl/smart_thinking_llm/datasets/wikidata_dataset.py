import logging
from pathlib import Path
from collections import defaultdict
import joblib
import mmap
from tqdm import tqdm
from joblib import Parallel, delayed

from smart_thinking_llm.datasets.base_dataset import BaseDataset
from smart_thinking_llm.datasets.data_classes import (
    Entity,
    EntityID,
    Object,
    ObjectID,
    Relation,
    RelationID,
)
from smart_thinking_llm.utils import init_basic_logger


class WikiDataset(BaseDataset):
    def __init__(
        self,
        dataset_path: Path,
        entity_aliases_filepath: Path,
        relation_aliases_filepath: Path,
    ):
        super().__init__()
        self._entity_aliases_filepath = entity_aliases_filepath
        self._relation_aliases_filepath = relation_aliases_filepath
        self._dataset_path = dataset_path
        self.logger = init_basic_logger(__class__.__name__, logging.DEBUG)

        self.logger.debug("Start parsing entities aliases file...")
        self._id2entities = self._create_objects(self._entity_aliases_filepath)
        self.logger.debug("Start parsing relation aliases file...")
        self._id2relations = self._create_objects(self._relation_aliases_filepath)
        self.unique_objects = set(
            [obj for obj in self._id2entities.values()]
            + [obj for obj in self._id2entities.values()]
        )
        self.logger.debug("Start parsing dataset file...")
        self._dataset = self._read_dataset(self._dataset_path)
        self.logger.debug("Start creating entity2entity graph...")
        self._entity_to_entity = self._init_entity_to_entity_graph()
        self.logger.debug("Dataset creation done!")

    def _create_objects(self, filepath: Path) -> dict[ObjectID, Object]:
        id2object = dict()
        with open(filepath, encoding="utf-8", mode="r") as file_:
            for line in file_:
                splitted_line = line.strip().split("\t")
                object_id = self._get_object_class(splitted_line[0])
                aliases = splitted_line[1:]
                if isinstance(object_id, EntityID):
                    id2object[object_id] = Entity(object_id, aliases)
                elif isinstance(object_id, RelationID):
                    id2object[object_id] = Relation(object_id, aliases)
                else:
                    raise ValueError(
                        f"Invalid ObjectID: {type(object_id)}. Support only EntityID and RelationID."
                    )
        return id2object

    def get_all_children_of_entity(
        self, entity: Entity
    ) -> list[tuple[Relation, Entity]]:
        return [
            (self._id2relations[rel_id], self._id2entities[ent_id])
            for rel_id, ent_id in self._entity_to_entity.get(entity.id, [])  # type: ignore
        ]  # type: ignore

    def _init_entity_to_entity_graph(
        self,
    ) -> dict[EntityID, list[tuple[RelationID, EntityID]]]:
        entity_to_entity = defaultdict(list)

        # Работаем напрямую с self._dataset для избежания лишних вызовов
        for entity_1_id, relation_id, entity_2_id in tqdm(
            self._dataset, desc="Creating entity2entity graph", total=len(self._dataset)
        ):
            entity_to_entity[entity_1_id].append((relation_id, entity_2_id))

        # Преобразуем defaultdict обратно в обычный dict
        return dict(entity_to_entity)

    def _get_object_class(self, object_id: str) -> ObjectID:
        if object_id.startswith("Q"):
            return EntityID(object_id)
        elif object_id.startswith("P"):
            return RelationID(object_id)
        else:
            raise ValueError(f"Invalid object ID: {object_id}")

    def _read_dataset(
        self, dataset_path: Path
    ) -> list[tuple[EntityID, RelationID, EntityID]]:
        dataset = []
        # Создаем множества для быстрой проверки существования
        entities_set = set(self._id2entities.keys())
        relations_set = set(self._id2relations.keys())

        # Функция для обработки чанка строк файла
        def process_chunk(chunk_lines, chunk_position):
            chunk_results = []
            for line in tqdm(
                chunk_lines,
                desc=f"Processing chunk {chunk_position + 1} of dataset",
                total=len(chunk_lines),
                position=chunk_position + 1,
            ):
                if isinstance(line, bytes):
                    line = line.decode("utf-8")

                parts = line.strip().split("\t")
                if len(parts) != 3:
                    continue

                # Проверяем строки напрямую перед созданием объектов
                entity_1_id = EntityID(parts[0])
                relation_id = RelationID(parts[1])
                entity_2_id = EntityID(parts[2])
                if (
                    entity_1_id in entities_set
                    and relation_id in relations_set
                    and entity_2_id in entities_set
                ):
                    chunk_results.append((entity_1_id, relation_id, entity_2_id))

            return chunk_results

        try:
            raise Exception("Do not use mmap")
            # Используем mmap для эффективного чтения
            with open(dataset_path, "r+b") as file:
                mm = mmap.mmap(file.fileno(), 0)

                # Получаем все строки
                lines = []
                line = mm.readline()
                while line:
                    lines.append(line)
                    line = mm.readline()

                mm.close()

            # Разделяем на чанки для параллельной обработки
            num_cpus = joblib.cpu_count()
            chunk_size = max(1, len(lines) // (num_cpus * 4))  # Больше чанков, чем ядер
            chunks = [
                lines[i : i + chunk_size] for i in range(0, len(lines), chunk_size)
            ]

            # Параллельная обработка чанков
            results = Parallel(n_jobs=-1, backend="threading")(
                delayed(process_chunk)(chunk, i)
                for i, chunk in tqdm(
                    enumerate(chunks),
                    desc="Processing dataset chunks",
                    total=len(chunks),
                    leave=False,
                )
            )

            # Объединяем результаты
            for chunk_results in results:
                if chunk_results is not None:
                    dataset.extend(chunk_results)

        except Exception as e:
            self.logger.warning(
                f"Error using mmap, falling back to standard processing: {e}"
            )
            # Если mmap не работает, используем обычный метод
            with open(dataset_path, encoding="utf-8", mode="r") as file_:
                all_lines = file_.readlines()
                dataset = process_chunk(all_lines, 0)

        return dataset

    def _get_object_by_id(self, id_: ObjectID) -> Object:
        if isinstance(id_, EntityID):
            if not id_ in self._id2entities:
                raise KeyError(f"No entity with id {id_}")
            else:
                return self._id2entities[id_]
        elif isinstance(id_, RelationID):
            if not id_ in self._id2relations:
                raise KeyError(f"No relation with id {id_}")
            else:
                return self._id2relations[id_]
        else:
            raise ValueError(f"Bad object id. Got: {id_}")

    def __len__(self) -> int:
        return len(self._dataset)

    def get_object_by_str_id(self, id_: str) -> Object:
        if id_.startswith("Q"):
            return self._get_object_by_id(EntityID(id_))
        elif id_.startswith("P"):
            return self._get_object_by_id(RelationID(id_))
        else:
            raise ValueError(f"Bad object id. Got: {id_}")

    def __getitem__(self, indx: int) -> dict[str, Object]:
        entity_1 = self._get_object_by_id(self._dataset[indx][0])
        relation = self._get_object_by_id(self._dataset[indx][1])
        entity_2 = self._get_object_by_id(self._dataset[indx][2])
        return {"entity_1": entity_1, "relation": relation, "entity_2": entity_2}
