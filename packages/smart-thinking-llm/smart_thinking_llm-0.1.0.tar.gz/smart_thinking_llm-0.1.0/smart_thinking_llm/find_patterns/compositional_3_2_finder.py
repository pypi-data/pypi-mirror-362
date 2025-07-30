import json
from pathlib import Path
from tqdm import trange

from smart_thinking_llm.datasets.data_classes import (
    Compositional32QuestionData,
    Entity,
    Relation,
)

from smart_thinking_llm.find_patterns.base_pattern_finder import BasePatternFinder
from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset


class Compositional32Finder(BasePatternFinder):
    def __init__(self, dataset: WikiDataset, black_list: set[str] | None = None):
        super().__init__(dataset, black_list)

    def format_pattern(self, question_data: Compositional32QuestionData) -> str:
        return json.dumps(question_data.to_id_dict())

    def find_patterns(self, output_file_path: Path, max_patterns: int) -> int:
        if output_file_path.name.split(".")[-1] != "json":
            raise ValueError("Output file must have .json extension")
        done_entities = set()
        for i in trange(len(self.dataset), desc="Finding compositional 3-2 patterns"):
            item = self.dataset[i]
            question_entity = item["entity_1"]
            answer_entity = item["entity_2"]
            question_relation = item["relation"]

            if not isinstance(question_entity, Entity) or not isinstance(answer_entity, Entity) or not isinstance(question_relation, Relation):
                continue

            if (
                self.is_blacklisted(question_entity)
                or self.is_blacklisted(answer_entity)
            ):
                continue
            for (
                relation_main_support_1,
                support_entity_1,
            ) in self.dataset.get_all_children_of_entity(question_entity):
                for (
                    relation_main_support_2,
                    support_entity_2,
                ) in self.dataset.get_all_children_of_entity(question_entity):
                    if not isinstance(support_entity_1, Entity) or not isinstance(support_entity_2, Entity):
                        continue
                    if support_entity_1 == support_entity_2:
                        continue

                    support_entity_1_children = self.dataset.get_all_children_of_entity(
                        support_entity_1
                    )
                    if len(support_entity_1_children) == 0:
                        continue
                    else:
                        relation_support_1, parent_support_entity_1 = (
                            support_entity_1_children[0]
                        )

                    support_entity_2_children = self.dataset.get_all_children_of_entity(
                        support_entity_2
                    )
                    if len(support_entity_2_children) == 0:
                        continue
                    else:
                        relation_support_2, parent_support_entity_2 = (
                            support_entity_2_children[0]
                        )

                    question_data = Compositional32QuestionData(
                        question_entity=question_entity,
                        answer_entity=answer_entity,
                        question_relation=question_relation,
                        support_entity_1=support_entity_1,
                        relation_main_support_1=relation_main_support_1,
                        support_entity_2=support_entity_2,
                        relation_main_support_2=relation_main_support_2,
                        parent_support_entity_1=parent_support_entity_1,
                        relation_support_1=relation_support_1,
                        parent_support_entity_2=parent_support_entity_2,
                        relation_support_2=relation_support_2,
                    )

                    if question_data in done_entities:
                        continue

                    done_entities.add(question_data)
                    if len(done_entities) > max_patterns:
                        with open(output_file_path, mode="w", encoding="utf-8") as out_file:
                            json.dump(
                                [question_data.to_id_dict() for question_data in done_entities],
                                out_file,
                                indent=4,
                            )
                        return len(done_entities)

        with open(output_file_path, mode="w", encoding="utf-8") as out_file:
            json.dump(
                [question_data.to_id_dict() for question_data in done_entities],
                out_file,
                indent=4,
            )
        return len(done_entities)
