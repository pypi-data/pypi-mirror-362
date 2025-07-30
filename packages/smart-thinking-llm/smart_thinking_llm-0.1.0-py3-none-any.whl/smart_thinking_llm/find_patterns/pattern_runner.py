import argparse
import logging
from pathlib import Path

from smart_thinking_llm.find_patterns import (
    Compositional32Finder,
    TwoHopPatternFinder,
    ThreeHopPatternFinder,
)
from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset
from smart_thinking_llm.utils import init_basic_logger

# Инициализируем глобальный логгер для этого модуля
logger = init_basic_logger(__name__, logging.INFO)


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Поиск паттернов в графе знаний")

    parser.add_argument(
        "--pattern_type",
        type=str,
        choices=["2hop", "3hop", "compositional_3_2"],
        required=True,
        help="Тип паттерна для поиска: 2hop (два шага) или 3hop (три шага)",
    )

    # Параметры для создания WikiDataset
    parser.add_argument(
        "--dataset_path",
        type=Path,
        required=True,
        help="Путь к файлу с датасетом WikiData (тройки)",
    )

    parser.add_argument(
        "--entity_aliases_path",
        type=Path,
        required=True,
        help="Путь к файлу с aliases сущностей",
    )

    parser.add_argument(
        "--relation_aliases_path",
        type=Path,
        required=True,
        help="Путь к файлу с aliases отношений",
    )

    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Путь к выходному файлу для сохранения результатов",
    )

    parser.add_argument(
        "--max_patterns",
        type=int,
        default=30000,
        help="Максимальное количество паттернов для поиска (по умолчанию: 30000)",
    )

    parser.add_argument(
        "--black_list",
        nargs="*",
        default=["Q5"],
        help="Список исключаемых сущностей (по умолчанию: Q5)",
    )

    # Дополнительные параметры для 3hop
    parser.add_argument(
        "--random_sample_size",
        type=int,
        default=2,
        help="Размер случайной выборки для 3hop поиска (по умолчанию: 2)",
    )

    return parser.parse_args()


def create_pattern_finder(
    pattern_type: str, dataset: WikiDataset, black_list: set[str], **kwargs
):
    """Создает соответствующий finder в зависимости от типа паттерна"""
    logger.info(f"Создание finder для типа паттерна: {pattern_type}")

    if pattern_type == "2hop":
        finder = TwoHopPatternFinder(dataset=dataset, black_list=black_list)
    elif pattern_type == "3hop":
        random_sample_size = kwargs.get("random_sample_size", 2)
        finder = ThreeHopPatternFinder(
            dataset=dataset,
            black_list=black_list,
            random_sample_size=random_sample_size,
        )
    elif pattern_type == "compositional_3_2":
        finder = Compositional32Finder(dataset=dataset, black_list=black_list)
    else:
        error_msg = f"Неподдерживаемый тип паттерна: {pattern_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Finder {finder.__class__.__name__} создан успешно")
    return finder


def main():
    """Главная функция"""
    args = parse_args()

    logger.info("=== Запуск поиска паттернов в графе знаний ===")
    logger.info(f"Тип паттерна: {args.pattern_type}")
    logger.info(f"Путь к датасету: {args.dataset_path}")
    logger.info(f"Путь к entity aliases: {args.entity_aliases_path}")
    logger.info(f"Путь к relation aliases: {args.relation_aliases_path}")

    # Создаем WikiDataset
    logger.info("Загружаем WikiDataset...")
    try:
        dataset = WikiDataset(
            args.dataset_path,
            args.entity_aliases_path,
            args.relation_aliases_path,
        )
        logger.info(f"Датасет загружен успешно. Размер: {len(dataset)} троек")
    except Exception as e:
        logger.error(f"Ошибка при загрузке датасета: {e}")
        return

    # Создаем finder в зависимости от типа паттерна
    try:
        pattern_finder = create_pattern_finder(
            args.pattern_type,
            dataset,
            set(args.black_list),
            random_sample_size=args.random_sample_size,
        )
    except Exception as e:
        logger.error(f"Ошибка при создании pattern finder: {e}")
        return

    # Выполняем поиск паттернов
    logger.info("=== Начинаем поиск паттернов ===")
    logger.info(f"Выходной файл: {args.output_file}")
    logger.info(f"Максимальное количество паттернов: {args.max_patterns}")
    logger.info(f"Черный список: {args.black_list}")

    try:
        count = pattern_finder.find_patterns(args.output_file, args.max_patterns)
        logger.info(f"=== Поиск завершен успешно ===")
        logger.info(
            f"Найдено {count} паттернов. Результаты сохранены в файл {args.output_file}"
        )
    except Exception as e:
        logger.error(f"Ошибка при поиске паттернов: {e}")


if __name__ == "__main__":
    main()
