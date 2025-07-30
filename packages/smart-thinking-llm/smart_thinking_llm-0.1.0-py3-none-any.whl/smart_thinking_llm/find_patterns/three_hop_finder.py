import random
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset
from smart_thinking_llm.find_patterns.base_pattern_finder import BasePatternFinder


class ThreeHopPatternFinder(BasePatternFinder):
    """Класс для поиска трехшаговых паттернов (цепочек из трех троек)"""

    def __init__(
        self, dataset: WikiDataset, black_list: set[str] | None = None, random_sample_size: int = 2
    ):
        super().__init__(dataset, black_list)
        self.random_sample_size = random_sample_size
        self.logger.info(
            f"Инициализирован ThreeHopPatternFinder с random_sample_size={random_sample_size}"
        )

    def get_random_n_triples(
        self, triples: list[tuple[str, str, str]], n: int
    ) -> list[tuple[str, str, str]]:
        """Возвращает случайные n троек из списка троек"""
        copy_triples = triples.copy()
        random.shuffle(copy_triples)
        return copy_triples[:n]

    def format_pattern(
        self,
        first_triple: tuple[str, str, str],
        second_triple: tuple[str, str, str],
        third_triple: tuple[str, str, str],
    ) -> str:
        """Форматирует цепочку из трех троек в удобочитаемый вид"""
        return (
            f"{first_triple[0]}\t{first_triple[1]}\t{first_triple[2]}\t"
            + f"{second_triple[0]}\t{second_triple[1]}\t{second_triple[2]}\t"
            + f"{third_triple[0]}\t{third_triple[1]}\t{third_triple[2]}"
        )

    def find_patterns(self, output_file_path: Path, max_patterns: int) -> int:
        """
        Находит все трехшаговые паттерны в графе и сохраняет результаты в файл

        Args:
            output_file_path: Путь к файлу для сохранения результатов
            max_patterns: Максимальное количество паттернов для поиска

        Returns:
            Количество найденных паттернов
        """
        self.logger.info(
            f"Начинаем поиск трехшаговых паттернов. Максимум: {max_patterns}"
        )
        self.logger.info(f"Выходной файл: {output_file_path}")
        self.logger.info(f"Черный список: {self.black_list}")
        self.logger.info(f"Размер случайной выборки: {self.random_sample_size}")

        try:
            # Получение троек из датасета
            triples = self.get_all_triples()

            # Создаем индекс для быстрого поиска
            triples_by_start = self.build_triples_index(triples)

            # Создаем выходную директорию если не существует
            output_dir = Path("/".join(output_file_path.parts[:-1]))
            if not output_dir.exists():
                output_dir.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Создана выходная директория: {output_dir}")

            # Находим цепочки из трех троек и сразу записываем в файл
            chain_count = 0
            used_middle = defaultdict(bool)

            self.logger.info("Начинаем поиск трехшаговых паттернов...")

            with open(output_file_path, "w", encoding="utf-8") as out_file:
                for first_triple in tqdm(
                    triples, total=max_patterns, desc="Поиск 3-hop паттернов"
                ):
                    if chain_count >= max_patterns:
                        self.logger.info(f"Достигнут лимит паттернов: {max_patterns}")
                        break

                    mid_node = first_triple[2]  # Конец первой тройки
                    if used_middle[mid_node]:
                        continue
                    used_middle[mid_node] = True

                    # Если есть тройки, начинающиеся с этого узла
                    if mid_node in triples_by_start:
                        for second_triple in self.get_random_n_triples(
                            triples_by_start[mid_node], n=self.random_sample_size
                        ):
                            end_node = second_triple[2]  # Конец второй тройки
                            if used_middle[end_node]:
                                continue
                            used_middle[end_node] = True

                            # Если есть тройки, начинающиеся с конца второй тройки
                            if end_node in triples_by_start:
                                for third_triple in self.get_random_n_triples(
                                    triples_by_start[end_node],
                                    n=self.random_sample_size,
                                ):
                                    chain = self.format_pattern(
                                        first_triple, second_triple, third_triple
                                    )
                                    out_file.write(chain + "\n")
                                    chain_count += 1

            self.logger.info(
                f"Поиск завершен. Найдено {chain_count} трехшаговых паттернов"
            )
            return chain_count

        except Exception as e:
            self.logger.error(f"Произошла ошибка при поиске паттернов: {e}")
            return 0
