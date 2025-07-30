import json
from pathlib import Path
from tqdm import tqdm

from smart_thinking_llm.generation.base_question_generator import BaseQuestionGenerator
from smart_thinking_llm.tools.path_converter import convert_compositional_3_2_path
from smart_thinking_llm.utils import make_openai_request


class Compositional32QuestionGenerator(BaseQuestionGenerator):
    """Класс для генерации композиционных вопросов из 5 базовых вопросов"""

    def __init__(self, dataset, openai_client, model_name, prompt_template: str, question_eval_threshold: float = 0.9, price_path: Path | None = None):
        super().__init__(dataset, openai_client, model_name, question_eval_threshold, price_path)
        self.prompt_template = prompt_template

    def format_prompt(self, questions: list[dict]) -> str:
        """Форматирует промпт для генерации композиционного вопроса из 5 базовых вопросов"""
        if len(questions) != 5:
            raise ValueError(f"Ожидается ровно 5 вопросов, получено: {len(questions)}")
        
        return self.prompt_template % {
            "question_1": questions[0]["generated_question"],
            "answer_1": questions[0]["answer_aliase"],
            "question_2": questions[1]["generated_question"],
            "answer_2": questions[1]["answer_aliase"],
            "question_3": questions[2]["generated_question"],
            "answer_3": questions[2]["answer_aliase"],
            "question_4": questions[3]["generated_question"],
            "answer_4": questions[3]["answer_aliase"],
            "question_5": questions[4]["generated_question"],
            "answer_5": questions[4]["answer_aliase"],
        }

    def load_base_questions(self, input_path: Path) -> list[dict]:
        """Загружает базовые вопросы из JSON файла"""
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_compositional_patterns(self, patterns_path: Path) -> list[dict]:
        """Загружает композиционные паттерны из find_patterns.json"""
        with open(patterns_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def match_questions_to_patterns(self, questions: list[dict], patterns: list[dict]) -> list[list[dict]]:
        """Сопоставляет базовые вопросы с композиционными паттернами"""
        grouped_questions = []
        
        # Создаем индекс вопросов по тройкам (entity_1_id, relation_id, entity_2_id)
        questions_index = {}
        for question in questions:
            key = (question["entity_1_id"], question["relation_id"], question["entity_2_id"])
            if key not in questions_index:
                questions_index[key] = []
            questions_index[key].append(question)
        
        self.logger.info(f"Создан индекс для {len(questions_index)} уникальных троек")
        
        # Для каждого паттерна ищем соответствующие вопросы
        for pattern in patterns:
            pattern_questions = []
            
            # Определяем 5 ожидаемых троек для данного паттерна
            expected_triples = [
                # Тройка 1: parent_support_entity_1 -> relation_support_1 -> support_entity_1
                (pattern["parent_support_entity_1"], pattern["relation_support_1"], pattern["support_entity_1"]),
                # Тройка 2: parent_support_entity_2 -> relation_support_2 -> support_entity_2  
                (pattern["parent_support_entity_2"], pattern["relation_support_2"], pattern["support_entity_2"]),
                # Тройка 3: question_entity -> relation_main_support_1 -> support_entity_1
                (pattern["question_entity"], pattern["relation_main_support_1"], pattern["support_entity_1"]),
                # Тройка 4: question_entity -> relation_main_support_2 -> support_entity_2
                (pattern["question_entity"], pattern["relation_main_support_2"], pattern["support_entity_2"]),
                # Тройка 5: question_entity -> question_relation -> answer_entity
                (pattern["question_entity"], pattern["question_relation"], pattern["answer_entity"])
            ]
            
            # Ищем вопросы для каждой тройки
            for triple in expected_triples:
                if triple in questions_index:
                    # Берем первый найденный вопрос для данной тройки
                    pattern_questions.append(questions_index[triple][0])
                else:
                    self.logger.warning(f"Не найден вопрос для тройки: {triple}")
                    pattern_questions = None
                    break
            
            # Если найдены все 5 вопросов для паттерна
            if pattern_questions and len(pattern_questions) == 5:
                grouped_questions.append(pattern_questions)
            else:
                self.logger.debug(f"Пропускаем паттерн - найдено {len(pattern_questions) if pattern_questions else 0} из 5 вопросов")
        
        self.logger.info(f"Успешно сопоставлено {len(grouped_questions)} полных композиционных паттернов")
        return grouped_questions

    def generate_compositional_question(self, questions: list[dict]) -> dict | None:
        """Генерирует композиционный вопрос для группы из 5 базовых вопросов"""
        try:
            # Формируем промпт
            prompt = self.format_prompt(questions)
            
            # Делаем запрос к модели
            response = make_openai_request(self.openai_client, self.model_name, prompt, self.logger)
            if not response:
                return None

            # Оцениваем качество (используем ответ последнего вопроса как эталон)
            final_answer = questions[4]["answer_aliase"]
            quality_score = self.evaluate_question_quality(response, final_answer)
            
            if quality_score < self.question_eval_threshold:
                self.logger.debug(f"Пропускаем вопрос с низким качеством: {quality_score}")
                return None

            linear_path = " -> ".join([
                f"{q['entity_1_id']}-{q['relation_id']}-{q['entity_2_id']}"
                for q in questions
            ])

            return {
                "generated_question": response,
                "final_answer": final_answer,
                "eval_score": quality_score,
                "base_questions": [
                    {
                        "question": q["generated_question"],
                        "answer": q["answer_aliase"],
                        "entity_1_id": q.get("entity_1_id", ""),
                        "relation_id": q.get("relation_id", ""),
                        "entity_2_id": q.get("entity_2_id", "")
                    }
                    for q in questions
                ],
                "compositional_path": convert_compositional_3_2_path(linear_path)
            }

        except Exception as e:
            self.logger.error(f"Ошибка при генерации композиционного вопроса: {e}")
            return None

    def generate_questions(self, input_data: Path | list, output_path: Path, max_questions: int | None = None, **kwargs) -> int:
        """
        Генерирует композиционные вопросы из базовых вопросов
        
        Args:
            input_data: Путь к файлу с базовыми вопросами или список базовых вопросов
            output_path: Путь для сохранения результатов
            max_questions: Максимальное количество вопросов для генерации
            **kwargs: Дополнительные параметры, включая patterns_file
            
        Returns:
            Количество сгенерированных вопросов
        """
        self.logger.info("Начинаем генерацию композиционных вопросов")
        
        patterns_file = kwargs.get('patterns_file')
        if patterns_file is None:
            raise ValueError("Необходимо указать patterns_file с композиционными паттернами")
        
        # Получаем базовые вопросы
        if isinstance(input_data, Path):
            base_questions = self.load_base_questions(input_data)
            self.logger.info(f"Загружено {len(base_questions)} базовых вопросов из файла")
        elif isinstance(input_data, list):
            base_questions = input_data
            self.logger.info(f"Получено {len(base_questions)} базовых вопросов")
        else:
            raise ValueError(f"Неизвестный тип входных данных: {type(input_data)}")

        # Загружаем композиционные паттерны
        compositional_patterns = self.load_compositional_patterns(patterns_file)
        self.logger.info(f"Загружено {len(compositional_patterns)} композиционных паттернов")

        # Сопоставляем вопросы с паттернами
        grouped_questions = self.match_questions_to_patterns(base_questions, compositional_patterns)
        
        if max_questions:
            grouped_questions = grouped_questions[:max_questions]
            self.logger.info(f"Ограничиваем до {max_questions} групп")

        # Запрашиваем подтверждение стоимости
        if grouped_questions:
            try:
                # Создаем образец промпта для оценки стоимости
                sample_group = grouped_questions[0]
                sample_prompt = self.format_prompt(sample_group)
                
                # Запрашиваем подтверждение (оценка ~150 токенов на выход)
                if not self.price_computer.request_cost_confirmation(sample_prompt, len(grouped_questions), 150):
                    self.logger.info("Генерация отменена пользователем")
                    return 0
                    
            except Exception as e:
                self.logger.warning(f"Не удалось оценить стоимость: {e}")
                if not self.price_computer.create_fallback_confirmation():
                    return 0
        else:
            self.logger.info("Не найдено композиционных паттернов")
            return 0

        generated_questions = []
        
        for question_group in tqdm(grouped_questions, desc="Генерация композиционных вопросов"):
            question_data = self.generate_compositional_question(question_group)
            if question_data:
                generated_questions.append(question_data)

        # Сохраняем результаты
        self.save_results(generated_questions, output_path)
        
        self.logger.info(f"Генерация завершена. Создано {len(generated_questions)} композиционных вопросов")
        return len(generated_questions)