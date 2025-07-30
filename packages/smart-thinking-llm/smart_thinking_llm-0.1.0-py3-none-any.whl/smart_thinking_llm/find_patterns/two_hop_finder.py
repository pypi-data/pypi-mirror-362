from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

from smart_thinking_llm.find_patterns.base_pattern_finder import BasePatternFinder


class TwoHopPatternFinder(BasePatternFinder):
    """Класс для поиска двухшаговых паттернов (цепочек из двух троек)"""

    def format_pattern(
        self, first_triple: tuple[str, str, str], second_triple: tuple[str, str, str]
    ) -> str | None:
        """Форматирует шестерку в удобочитаемый вид"""
        return f"{first_triple[0]}\t{first_triple[1]}\t{first_triple[2]}\t{second_triple[0]}\t{second_triple[1]}\t{second_triple[2]}"

    def find_patterns(self, output_file_path: Path, max_patterns: int) -> int:
        """
        Находит все двухшаговые паттерны в графе и сохраняет результаты в файл

        Args:
            output_file_path: Путь к файлу для сохранения результатов
            max_patterns: Максимальное количество паттернов для поиска

        Returns:
            Количество найденных паттернов
        """
        self.logger.info(
            f"Начинаем поиск двухшаговых паттернов. Максимум: {max_patterns}"
        )
        self.logger.info(f"Выходной файл: {output_file_path}")
        self.logger.info(f"Черный список: {self.black_list}")

        try:
            # Получение троек из датасета
            triples = self.get_all_triples()

            # Создаем индекс для быстрого поиска
            triples_by_start = self.build_triples_index(triples)

            # Находим паттерны и сразу записываем в файл
            pattern_count = 0
            used_middle = defaultdict(bool)

            self.logger.info("Начинаем поиск двухшаговых паттернов...")

            with open(output_file_path, "w", encoding="utf-8") as out_file:
                for first_triple in tqdm(triples, desc="Поиск 2-hop паттернов"):
                    if pattern_count >= max_patterns:
                        self.logger.info(f"Достигнут лимит паттернов: {max_patterns}")
                        break

                    end_node = first_triple[2]  # Конец первой тройки

                    # Проверяем черный список и использованные узлы
                    if (
                        used_middle[end_node]
                        or self.is_blacklisted(end_node)
                        or self.is_blacklisted(first_triple[0])
                    ):
                        continue

                    used_middle[end_node] = True

                    # Если есть тройки, начинающиеся с конца первой тройки
                    if end_node in triples_by_start:
                        for second_triple in triples_by_start[end_node]:
                            if (
                                self.is_blacklisted(second_triple[0])
                                or self.is_blacklisted(second_triple[2])
                            ):
                                continue

                            pattern = self.format_pattern(first_triple, second_triple)
                            if pattern is not None:
                                out_file.write(pattern + "\n")
                            pattern_count += 1

            self.logger.info(
                f"Поиск завершен. Найдено {pattern_count} двухшаговых паттернов"
            )
            return pattern_count

        except Exception as e:
            self.logger.error(f"Произошла ошибка при поиске паттернов: {e}")
            return 0
