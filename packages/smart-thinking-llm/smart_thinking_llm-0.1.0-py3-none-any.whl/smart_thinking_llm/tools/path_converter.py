import argparse


def convert_compositional_3_2_path(path_string: str) -> str:
    """
    Преобразует линейный compositional_path для структуры 3_2
    в формат с группировкой параллельных веток.

    Пример:
    Вход: "T1 -> T2 -> T3 -> T4 -> T5"
    Выход: "((T1->T3), (T2->T4)) -> T5"

    Args:
        path_string: Строка пути, где триплеты разделены " -> ".

    Returns:
        Преобразованная строка с указанием зависимостей.

    Raises:
        ValueError: Если количество элементов в пути не равно 5.
    """
    triplets = path_string.split(" -> ")
    if len(triplets) != 5:
        raise ValueError(
            "Этот конвертер предназначен только для путей compositional_3_2, "
            f"которые состоят из 5 частей. Получено: {len(triplets)}"
        )

    t1, t2, t3, t4, t5 = triplets

    # Согласно структуре compositional_3_2:
    # 1-й и 3-й вопросы образуют одну ветку.
    # 2-й и 4-й вопросы образуют вторую ветку.
    # Обе ветки используются для модификации 5-го вопроса.
    formatted_path = f"(({t1}->{t3}), ({t2}->{t4})) -> {t5}"
    return formatted_path


def main():
    """
    Основная функция для запуска скрипта из командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Конвертировать линейный compositional path в структурированный формат.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "path_string",
        type=str,
        help='Строка пути в кавычках. \nПример: "Q1-R1-E1 -> Q2-R2-E2 -> Q3-R3-E3 -> Q4-R4-E4 -> Q5-R5-E5"',
    )

    args = parser.parse_args()

    try:
        converted_path = convert_compositional_3_2_path(args.path_string)
        print("Исходный путь:")
        print(f"  {args.path_string}")
        print("\nПреобразованный путь:")
        print(f"  {converted_path}")
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main() 