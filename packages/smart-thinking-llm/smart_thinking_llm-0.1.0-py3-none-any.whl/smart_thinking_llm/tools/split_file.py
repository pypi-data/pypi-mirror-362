import argparse


def extract_first_n_lines(input_file: str, output_file: str, n: int):
    """
    Извлекает первые n строк из входного файла и сохраняет их в выходной файл.

    Args:
        input_file (str): Путь к входному файлу
        output_file (str): Путь к выходному файлу
        n (int): Количество строк для извлечения
    """
    try:
        count = 0
        with open(input_file, "r", encoding="utf-8") as in_file, open(
            output_file, "w", encoding="utf-8"
        ) as out_file:
            for i, line in enumerate(in_file):
                if i >= n:
                    break
                out_file.write(line)
                count += 1

        print(f"Успешно извлечено {count} строк из {input_file} в {output_file}")

    except Exception as e:
        print(f"Ошибка: {e}")


def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Извлечь первые n строк из файла")
    parser.add_argument("--input_file", help="Путь к входному файлу")
    parser.add_argument("--output_file", help="Путь к выходному файлу")
    parser.add_argument("--n", type=int, help="Количество строк для извлечения")

    # Разбор аргументов
    args = parser.parse_args()

    # Вызов функции извлечения строк
    extract_first_n_lines(args.input_file, args.output_file, args.n)


if __name__ == "__main__":
    main()
