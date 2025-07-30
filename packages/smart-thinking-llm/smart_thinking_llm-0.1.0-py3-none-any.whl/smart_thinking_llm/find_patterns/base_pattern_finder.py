from abc import ABC, abstractmethod
from collections import defaultdict
import logging
from pathlib import Path
from tqdm import tqdm

from smart_thinking_llm.datasets.data_classes import Entity
from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset
from smart_thinking_llm.utils import init_basic_logger


class BasePatternFinder(ABC):
    """Базовый класс для поиска паттернов в графе знаний"""

    def __init__(self, dataset: WikiDataset, black_list: set[str] | None = None):
        self.dataset = dataset
        self.black_list = black_list or {"Q5"}
        self.logger = init_basic_logger(self.__class__.__name__, logging.DEBUG)

    def get_all_triples(self) -> list[tuple[str, str, str]]:
        """Получает все тройки из датасета в виде строк"""
        self.logger.info(f"Извлечение троек из датасета размером {len(self.dataset)}")
        triples = []
        for i in tqdm(range(len(self.dataset)), desc="Извлечение троек"):
            item = self.dataset[i]
            triple = (
                str(item["entity_1"].id),
                str(item["relation"].id),
                str(item["entity_2"].id),
            )
            triples.append(triple)
        self.logger.info(f"Извлечено {len(triples)} троек")
        return triples

    def build_triples_index(
        self, triples: list[tuple[str, str, str]]
    ) -> dict[str, list[tuple[str, str, str]]]:
        """Создает индекс троек по начальному узлу"""
        self.logger.debug("Создание индекса троек по начальному узлу")
        triples_by_start = defaultdict(list)
        for triple in triples:
            start_node = triple[0]
            triples_by_start[start_node].append(triple)
        self.logger.debug(
            f"Создан индекс для {len(triples_by_start)} уникальных начальных узлов"
        )
        return triples_by_start

    def is_blacklisted(self, entity: Entity | str) -> bool:
        """Проверяет, находится ли сущность в черном списке"""
        if isinstance(entity, Entity):
            return str(entity.id) in self.black_list
        else:
            return entity in self.black_list

    @abstractmethod
    def find_patterns(self, output_file_path: Path, max_patterns: int) -> int:
        """Абстрактный метод для поиска паттернов"""
        pass

    @abstractmethod
    def format_pattern(self, *args) -> str:
        """Абстрактный метод для форматирования найденного паттерна"""
        pass
