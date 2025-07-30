from abc import ABC, abstractmethod
import json
import logging
from pathlib import Path

import openai
from smart_thinking_llm.datasets.wikidata_dataset import WikiDataset
from smart_thinking_llm.utils import QuestionQualityMetric, init_basic_logger
from smart_thinking_llm.generation.price_computer import PriceComputer


class BaseQuestionGenerator(ABC):
    """Базовый класс для генерации вопросов"""

    def __init__(
        self,
        dataset: WikiDataset,
        openai_client: openai.OpenAI,
        model_name: str,
        question_eval_threshold: float = 0.9,
        price_path: Path | None = None,
    ):
        self.dataset = dataset
        self.openai_client = openai_client
        self.model_name = model_name
        self.question_eval_threshold = question_eval_threshold
        self.quality_metric = QuestionQualityMetric(openai_client, model_name)
        self.logger = init_basic_logger(self.__class__.__name__, logging.DEBUG)
        
        # Определяем путь к файлу цен
        if price_path is None:
            # Используем стандартное расположение относительно текущего модуля
            current_dir = Path(__file__).parent.parent
            price_path = current_dir / "prices.json"
        
        # Создаем компьютер для подсчета стоимости
        self.price_computer = PriceComputer(model_name, price_path)

    def load_prompt_template(self, prompt_path: Path) -> str:
        """Загружает шаблон промпта из файла"""
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def save_results(self, results: list[dict], output_path: Path) -> None:
        """Сохраняет результаты в JSON файл"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        self.logger.info(f"Результаты сохранены в {output_path}")

    def evaluate_question_quality(self, question: str, answer: str) -> float:
        """Оценивает качество сгенерированного вопроса"""
        try:
            return self.quality_metric.measure(question, answer)
        except Exception as e:
            self.logger.error(f"Ошибка при оценке качества вопроса: {e}")
            return 0.0

    @abstractmethod
    def generate_questions(
        self, input_data: Path | list, output_path: Path, max_questions: int | None = None, **kwargs
    ) -> int:
        """Абстрактный метод для генерации вопросов"""
        pass

    @abstractmethod
    def format_prompt(self, *args, **kwargs) -> str:
        """Абстрактный метод для форматирования промпта"""
        pass
