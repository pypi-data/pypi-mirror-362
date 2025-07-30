import json
from pathlib import Path
from tqdm import tqdm

from smart_thinking_llm.datasets.data_classes import Entity, Relation
from smart_thinking_llm.generation.base_question_generator import BaseQuestionGenerator
from smart_thinking_llm.utils import make_openai_request


class BasicQuestionGenerator(BaseQuestionGenerator):
    """Класс для генерации базовых вопросов из троек"""

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
        self,
        entity_1_aliases: list[str],
        relation_aliases: list[str],
        entity_2_aliases: list[str],
    ) -> str:
        """Форматирует промпт для генерации базового вопроса"""
        return self.prompt_template % (
            entity_1_aliases,
            relation_aliases,
            entity_2_aliases,
        )

    def parse_response(self, response: str) -> tuple[str, str, str, str] | None:
        """Парсит ответ модели на компоненты"""
        try:
            parts = response.split(" [END] ")
            if len(parts) == 4:
                return parts[0], parts[1], parts[2], parts[3]
            else:
                self.logger.warning(f"Неверный формат ответа: {response}")
                return None
        except Exception as e:
            self.logger.error(f"Ошибка при парсинге ответа: {e}")
            return None

    def generate_question_for_triple(
        self, entity_1_id: str, relation_id: str, entity_2_id: str
    ) -> dict | None:
        """Генерирует вопрос для одной тройки"""
        try:
            # Получаем объекты из датасета
            entity_1 = self.dataset.get_object_by_str_id(entity_1_id)
            relation = self.dataset.get_object_by_str_id(relation_id)
            entity_2 = self.dataset.get_object_by_str_id(entity_2_id)

            if not (isinstance(entity_1, (Entity, Relation)) and isinstance(relation, Relation) and isinstance(entity_2, (Entity, Relation))):
                self.logger.warning(f"Некорректные типы для тройки: {entity_1_id}-{relation_id}-{entity_2_id}")
                return None

            # Формируем промпт
            prompt = self.format_prompt(
                entity_1.aliases, relation.aliases, entity_2.aliases
            )

            # Делаем запрос к модели
            response = make_openai_request(self.openai_client, self.model_name, prompt, self.logger)
            if not response:
                return None

            # Парсим ответ
            parsed = self.parse_response(response)
            if not parsed:
                return None

            subject_aliase, content_aliase, question, answer_aliase = parsed

            # Оцениваем качество
            quality_score = self.evaluate_question_quality(question, answer_aliase)

            if quality_score < self.question_eval_threshold:
                self.logger.debug(
                    f"Пропускаем вопрос с низким качеством: {quality_score}"
                )
                return None

            return {
                "subject_aliase": subject_aliase,
                "content_aliase": content_aliase,
                "generated_question": question,
                "answer_aliase": answer_aliase,
                "entity_1_id": entity_1_id,
                "relation_id": relation_id,
                "entity_2_id": entity_2_id,
                "eval_score": quality_score,
            }

        except Exception as e:
            self.logger.error(
                f"Ошибка при генерации вопроса для тройки {entity_1_id}-{relation_id}-{entity_2_id}: {e}"
            )
            return None

    def load_triples_from_file(self, input_path: Path) -> list[tuple[str, str, str]]:
        """Загружает тройки из файла"""
        triples = []

        if input_path.suffix == ".json":
            # Загружаем из JSON (результат compositional finder)
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    # Извлекаем 5 уникальных троек для compositional_32 генерации
                    unique_triples = set()
                    
                    # Тройка 1: parent_support_entity_1 -> relation_support_1 -> support_entity_1 
                    unique_triples.add(
                        (
                            item["parent_support_entity_1"],
                            item["relation_support_1"],
                            item["support_entity_1"],
                        )
                    )
                    
                    # Тройка 2: parent_support_entity_2 -> relation_support_2 -> support_entity_2
                    unique_triples.add(
                        (
                            item["parent_support_entity_2"],
                            item["relation_support_2"],
                            item["support_entity_2"],
                        )
                    )
                    
                    # Тройка 3: question_entity -> relation_main_support_1 -> support_entity_1
                    unique_triples.add(
                        (
                            item["question_entity"],
                            item["relation_main_support_1"],
                            item["support_entity_1"],
                        )
                    )
                    
                    # Тройка 4: question_entity -> relation_main_support_2 -> support_entity_2
                    unique_triples.add(
                        (
                            item["question_entity"],
                            item["relation_main_support_2"],
                            item["support_entity_2"],
                        )
                    )
                    
                    # Тройка 5: question_entity -> question_relation -> answer_entity
                    unique_triples.add(
                        (
                            item["question_entity"],
                            item["question_relation"],
                            item["answer_entity"],
                        )
                    )
                    
                    triples.extend(list(unique_triples))
        else:
            # Загружаем из TSV (результат pattern finder)
            with open(input_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 6:  # 2-hop: 6 элементов
                        # Первая тройка
                        triples.append((parts[0], parts[1], parts[2]))
                        # Вторая тройка
                        triples.append((parts[3], parts[4], parts[5]))

                        if len(parts) >= 9:  # 3-hop: 9 элементов
                            # Третья тройка
                            triples.append((parts[6], parts[7], parts[8]))

        # Удаляем дубликаты
        return list(set(triples))

    def generate_questions(
        self, input_data: Path | list, output_path: Path, max_questions: int | None = None, **kwargs
    ) -> int:
        """
        Генерирует базовые вопросы из троек

        Args:
            input_data: Путь к файлу с тройками или список троек
            output_path: Путь для сохранения результатов
            max_questions: Максимальное количество вопросов для генерации

        Returns:
            Количество сгенерированных вопросов
        """
        self.logger.info("Начинаем генерацию базовых вопросов")

        # Получаем тройки
        if isinstance(input_data, Path):
            triples = self.load_triples_from_file(input_data)
            self.logger.info(f"Загружено {len(triples)} уникальных троек из файла")
        else:
            triples = input_data
            self.logger.info(f"Получено {len(triples)} троек")

        if max_questions:
            triples = triples[:max_questions]
            self.logger.info(f"Ограничиваем до {max_questions} троек")

        # Запрашиваем подтверждение стоимости
        if triples:
            # Создаем образец промпта для оценки стоимости
            try:
                # Берем первую тройку для создания образца
                sample_entity_1_id, sample_relation_id, sample_entity_2_id = triples[0]
                sample_entity_1 = self.dataset.get_object_by_str_id(sample_entity_1_id)
                sample_relation = self.dataset.get_object_by_str_id(sample_relation_id)
                sample_entity_2 = self.dataset.get_object_by_str_id(sample_entity_2_id)

                if not (isinstance(sample_entity_1, (Entity, Relation)) and isinstance(sample_relation, Relation) and isinstance(sample_entity_2, (Entity, Relation))):
                    self.logger.warning(f"Не удалось создать образец промпта, некорректные типы")
                    if not self.price_computer.create_fallback_confirmation():
                        return 0
                    return 0 # Should not proceed if types are wrong
                
                sample_prompt = self.format_prompt(
                    sample_entity_1.aliases,
                    sample_relation.aliases,
                    sample_entity_2.aliases,
                )
                
                # Запрашиваем подтверждение (оценка ~150 токенов на выход)
                if not self.price_computer.request_cost_confirmation(sample_prompt, len(triples), 150):
                    self.logger.info("Генерация отменена пользователем")
                    return 0
                    
            except Exception as e:
                self.logger.warning(f"Не удалось оценить стоимость: {e}")
                if not self.price_computer.create_fallback_confirmation():
                    return 0

        generated_questions = []

        for entity_1_id, relation_id, entity_2_id in tqdm(
            triples, desc="Генерация базовых вопросов"
        ):
            question_data = self.generate_question_for_triple(
                entity_1_id, relation_id, entity_2_id
            )
            if question_data:
                generated_questions.append(question_data)

        # Сохраняем результаты
        self.save_results(generated_questions, output_path)

        self.logger.info(
            f"Генерация завершена. Создано {len(generated_questions)} вопросов"
        )
        return len(generated_questions)
