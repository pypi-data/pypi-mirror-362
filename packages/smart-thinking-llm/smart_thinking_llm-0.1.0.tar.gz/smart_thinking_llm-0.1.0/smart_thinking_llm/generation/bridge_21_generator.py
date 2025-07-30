import json
from collections import defaultdict
from pathlib import Path
import threading
from tqdm import tqdm

from smart_thinking_llm.generation.base_question_generator import BaseQuestionGenerator
from smart_thinking_llm.utils import make_openai_request


class Bridge21Generator(BaseQuestionGenerator):
    """Класс для генерации Bridge 2-1 вопросов (объединение двух вопросов в один)"""

    def __init__(
        self,
        dataset,
        openai_client,
        model_name,
        prompt_template: str,
        question_eval_threshold: float = 0.9,
        price_path: Path | None = None,
    ):
        super().__init__(dataset, openai_client, model_name, question_eval_threshold, price_path)
        self.prompt_template = prompt_template

    def format_prompt(
        self, question_1: str, answer_1: str, question_2: str, answer_2: str
    ) -> str:
        """Форматирует промпт для объединения двух вопросов"""
        return self.prompt_template % {
            "question_1": question_1,
            "answer_1": answer_1,
            "question_2": question_2,
            "answer_2": answer_2,
        }

    def load_base_questions(self, input_path: Path) -> list[dict]:
        """Загружает базовые вопросы из JSON файла"""
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def find_compatible_pairs(self, questions: list[dict]) -> list[tuple[int, int]]:
        """Находит совместимые пары вопросов (где answer первого = entity_1_id второго)"""
        compatible_pairs = []

        self.logger.info("Поиск совместимых пар вопросов...")

        for i, q1 in enumerate(questions):
            for j, q2 in enumerate(questions):
                if i != j and "entity_2_id" in q1 and "entity_1_id" in q2:
                    if q1["entity_2_id"] == q2["entity_1_id"]:
                        compatible_pairs.append((i, j))

        self.logger.info(f"Найдено {len(compatible_pairs)} совместимых пар")
        return compatible_pairs

    def generate_bridge_question(self, q1: dict, q2: dict) -> dict | None:
        """Генерирует объединенный вопрос для пары базовых вопросов"""
        try:
            # Формируем промпт
            prompt = self.format_prompt(
                q1["generated_question"],
                q1["answer_aliase"],
                q2["generated_question"],
                q2["answer_aliase"],
            )

            # Делаем запрос к модели
            response = make_openai_request(self.openai_client, self.model_name, prompt, self.logger)
            if not response:
                return None

            # Оцениваем качество
            quality_score = self.evaluate_question_quality(
                response, q2["answer_aliase"]
            )

            if quality_score < self.question_eval_threshold:
                self.logger.debug(
                    f"Пропускаем вопрос с низким качеством: {quality_score}"
                )
                return None

            return {
                "generated_question": response,
                "first_question": q1["generated_question"],
                "first_answer": q1["answer_aliase"],
                "second_question": q2["generated_question"],
                "second_answer": q2["answer_aliase"],
                "score": quality_score,
                "path": f"{q1['entity_1_id']} -> {q1['relation_id']} -> {q1['entity_2_id']} -> {q2['relation_id']} -> {q2['entity_2_id']}",
            }

        except Exception as e:
            self.logger.error(f"Ошибка при генерации bridge вопроса: {e}")
            return None

    def generate_questions(
        self,
        input_data: Path | list,
        output_path: Path,
        max_questions: int | None = None,
        max_per_middle: int = 10,
        **kwargs
    ) -> int:
        """
        Генерирует Bridge 2-1 вопросы

        Args:
            input_data: Путь к файлу с базовыми вопросами или список базовых вопросов
            output_path: Путь для сохранения результатов
            max_questions: Максимальное количество вопросов для генерации
            max_per_middle: Максимальное количество вопросов на средний узел
        Returns:
            Количество сгенерированных вопросов
        """
        self.logger.info("Начинаем генерацию Bridge 2-1 вопросов")

        # Загружаем базовые вопросы
        if isinstance(input_data, Path):
            base_questions = self.load_base_questions(input_data)
        else:
            base_questions = input_data

        self.logger.info(f"Загружено {len(base_questions)} базовых вопросов")

        # Находим совместимые пары
        compatible_pairs = self.find_compatible_pairs(base_questions)

        if max_questions:
            compatible_pairs = compatible_pairs[:max_questions]
            self.logger.info(f"Ограничиваем до {max_questions} пар")

        # Запрашиваем подтверждение стоимости
        if compatible_pairs and base_questions:
            try:
                # Создаем образец промпта для оценки стоимости
                i, j = compatible_pairs[0]
                q1 = base_questions[i]
                q2 = base_questions[j]
                
                sample_prompt = self.format_prompt(
                    q1["generated_question"],
                    q1["answer_aliase"],
                    q2["generated_question"],
                    q2["answer_aliase"],
                )
                
                # Запрашиваем подтверждение (оценка ~80 токенов на выход)
                if not self.price_computer.request_cost_confirmation(sample_prompt, len(compatible_pairs), 80):
                    self.logger.info("Генерация отменена пользователем")
                    return 0
                    
            except Exception as e:
                self.logger.warning(f"Не удалось оценить стоимость: {e}")
                if not self.price_computer.create_fallback_confirmation():
                    return 0

        generated_questions = []
        done_middle_count = defaultdict(int)

        for i, j in tqdm(compatible_pairs, desc="Генерация Bridge 2-1 вопросов"):
            q1 = base_questions[i]
            q2 = base_questions[j]

            middle_entity_id = q1["entity_2_id"]

            # Проверяем лимит на средний узел
            if done_middle_count[middle_entity_id] >= max_per_middle:
                continue

            bridge_question = self.generate_bridge_question(q1, q2)
            if bridge_question:
                generated_questions.append(bridge_question)
                done_middle_count[middle_entity_id] += 1

        # Сохраняем результаты
        self.save_results(generated_questions, output_path)

        self.logger.info(
            f"Генерация завершена. Создано {len(generated_questions)} Bridge 2-1 вопросов"
        )
        return len(generated_questions)
