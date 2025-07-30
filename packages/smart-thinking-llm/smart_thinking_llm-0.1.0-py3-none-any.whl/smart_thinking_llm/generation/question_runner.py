import argparse
import logging
import os
from pathlib import Path

import openai
from dotenv import load_dotenv

from smart_thinking_llm.generation.basic_question_generator import BasicQuestionGenerator
from smart_thinking_llm.generation.bridge_21_generator import Bridge21Generator
from smart_thinking_llm.generation.bridge_31_generator import Bridge31Generator
from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset
from smart_thinking_llm.generation.compositional_question_generator import Compositional32QuestionGenerator
from smart_thinking_llm.utils import init_basic_logger

# Инициализируем глобальный логгер для этого модуля
logger = init_basic_logger(__name__, logging.INFO)


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Генерация вопросов по паттернам")

    parser.add_argument(
        "--generator_type",
        type=str,
        choices=["basic", "bridge_21", "bridge_31", "compositional32"],
        required=True,  
        help="Тип генератора вопросов",
    )

    # Параметры для создания WikiDataset
    parser.add_argument(
        "--dataset_path",
        type=Path,
        default=Path("data/raw_data/wikidata5m_transductive/wikidata5m_transductive_train.txt"),
        help="Путь к файлу с датасетом WikiData (тройки)",
    )

    parser.add_argument(
        "--entity_aliases_path",
        type=Path,
        default=Path("data/raw_data/wikidata5m_alias/wikidata5m_entity.txt"),
        help="Путь к файлу с aliases сущностей",
    )

    parser.add_argument(
        "--relation_aliases_path",
        type=Path,
        default=Path("data/raw_data/wikidata5m_alias/wikidata5m_relation.txt"),
        help="Путь к файлу с aliases отношений",
    )

    # Входные данные
    parser.add_argument(
        "--input_file",
        type=Path,
        required=True,
        help="Путь к входному файлу (тройки для basic, базовые вопросы для bridge и compositional32)",
    )

    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Путь к выходному файлу для сохранения результатов",
    )

    # Параметры OpenAI
    parser.add_argument(
        "--openai_api_key",
        type=str,
        default=os.environ.get("OPENAI_APIKEY"),
        help="Ключ API OpenAI",
    )

    parser.add_argument(
        "--openai_model_name",
        type=str,
        default="gpt-4.1-mini",
        choices=["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"],
        help="Имя модели OpenAI",
    )

    # Промпт
    parser.add_argument(
        "--prompt_template_path",
        type=Path,
        help="Путь к файлу с шаблоном промпта",
    )

    parser.add_argument(
        "--price_path",
        type=Path,
        help="Путь к файлу с ценами на API (по умолчанию: smart_thinking_llm/prices.json)",
    )

    parser.add_argument(
        "--max_questions",
        type=int,
        required=True,
        help="Максимальное количество вопросов для генерации",
    )

    parser.add_argument(
        "--question_eval_threshold",
        type=float,
        default=0.9,
        help="Порог для оценки качества вопроса",
    )

    # Дополнительные параметры для compositional32
    parser.add_argument(
        "--patterns_file",
        type=Path,
        help="Путь к файлу find_patterns.json для compositional32 генератора",
    )

    return parser.parse_args()


def load_prompt_template(prompt_template_path: Path | None = None) -> str:
    """Загружает шаблон промпта из файла или возвращает переданную строку"""
    if prompt_template_path:
        with open(prompt_template_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Необходимо указать prompt_template_path")


def create_question_generator(
    generator_type: str,
    dataset: WikiDataset,
    openai_client: openai.OpenAI,
    model_name: str,
    prompt_template: str,
    question_eval_threshold: float,
    price_path: Path | None = None,
):
    """Создает соответствующий генератор в зависимости от типа"""
    logger.info(f"Создание генератора для типа: {generator_type}")

    if generator_type == "basic":
        generator = BasicQuestionGenerator(
            dataset=dataset,
            openai_client=openai_client,
            model_name=model_name,
            prompt_template=prompt_template,
            question_eval_threshold=question_eval_threshold,
            price_path=price_path,
        )
    elif generator_type == "bridge_21":
        generator = Bridge21Generator(
            dataset=dataset,
            openai_client=openai_client,
            model_name=model_name,
            prompt_template=prompt_template,
            question_eval_threshold=question_eval_threshold,
            price_path=price_path,
        )
    elif generator_type == "bridge_31":
        generator = Bridge31Generator(
            dataset=dataset,
            openai_client=openai_client,
            model_name=model_name,
            prompt_template=prompt_template,
            question_eval_threshold=question_eval_threshold,
            price_path=price_path,
        )
    elif generator_type == "compositional32":
        generator = Compositional32QuestionGenerator(
            dataset=dataset,
            openai_client=openai_client,
            model_name=model_name,
            prompt_template=prompt_template,
            question_eval_threshold=question_eval_threshold,
            price_path=price_path,
        )
    else:
        error_msg = f"Неподдерживаемый тип генератора: {generator_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Генератор {generator.__class__.__name__} создан успешно")
    return generator


def main():
    """Главная функция"""
    load_dotenv()
    args = parse_args()

    # Для compositional32 генератора передаем дополнительный параметр
    if args.generator_type == "compositional32":
        if args.patterns_file is None:
            logger.error("Для compositional32 генератора необходимо указать --patterns_file")
            return

    logger.info("=== Запуск генерации вопросов ===")
    logger.info(f"Тип генератора: {args.generator_type}")
    logger.info(f"Входной файл: {args.input_file}")
    logger.info(f"Выходной файл: {args.output_file}")

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

    # Создаем OpenAI клиент
    try:
        openai_client = openai.OpenAI(api_key=args.openai_api_key)
        logger.info("OpenAI клиент создан успешно")
    except Exception as e:
        logger.error(f"Ошибка при создании OpenAI клиента: {e}")
        return

    # Загружаем шаблон промпта
    try:
        prompt_template = load_prompt_template(args.prompt_template_path)
        logger.info("Шаблон промпта загружен успешно")
    except Exception as e:
        logger.error(f"Ошибка при загрузке шаблона промпта: {e}")
        return

    # Создаем генератор
    try:
        question_generator = create_question_generator(
            args.generator_type,
            dataset,
            openai_client,
            args.openai_model_name,
            prompt_template,
            args.question_eval_threshold,
            args.price_path,
        )
    except Exception as e:
        logger.error(f"Ошибка при создании генератора: {e}")
        return

    # Выполняем генерацию вопросов
    logger.info("=== Начинаем генерацию вопросов ===")
    logger.info(f"Максимальное количество вопросов: {args.max_questions}")
    logger.info(f"Порог качества: {args.question_eval_threshold}")

    try:
        count = question_generator.generate_questions(
            args.input_file, args.output_file, args.max_questions, patterns_file=args.patterns_file
        )
        logger.info(f"=== Генерация завершена успешно ===")
        logger.info(
            f"Сгенерировано {count} вопросов. Результаты сохранены в файл {args.output_file}"
        )
    except Exception as e:
        logger.error(f"Ошибка при генерации вопросов: {e}")


if __name__ == "__main__":
    main()