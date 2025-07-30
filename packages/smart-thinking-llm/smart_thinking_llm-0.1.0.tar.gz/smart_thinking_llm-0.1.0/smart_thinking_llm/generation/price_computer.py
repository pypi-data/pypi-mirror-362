import json
import logging
from pathlib import Path
from typing import Any

from smart_thinking_llm.utils import init_basic_logger


class PriceComputer:
    """Класс для подсчета стоимости API запросов"""

    def __init__(self, model_name: str, price_path: Path):
        self.model_name = model_name
        self.price_path = price_path
        self.logger = init_basic_logger(self.__class__.__name__, logging.DEBUG)
        self.pricing_data = self.load_pricing_data()

    def map_model_name(self, model_name: str) -> str:
        """
        Маппит полное название модели к базовому названию в файле цен
        путем поиска подстрок из prices.json в названии модели.
        
        Примеры:
        - gpt-4o-mini-2024-07-18 содержит "gpt-4o-mini" -> gpt-4o-mini
        - gpt-4.1-turbo-preview содержит "gpt-4.1" -> gpt-4.1
        - gpt-3.5-turbo-0125 содержит "gpt-3.5-turbo" -> gpt-3.5-turbo
        """
        # Получаем все доступные названия моделей из файла цен
        available_models = list(self.pricing_data.keys())
        
        # Ищем все подстроки из available_models, которые содержатся в model_name
        matching_models = []
        for available_model in available_models:
            if available_model in model_name:
                matching_models.append(available_model)
        
        if not matching_models:
            # Если ничего не найдено, возвращаем исходное название
            self.logger.debug(f"Маппинг не найден для модели: {model_name}, используем как есть")
            return model_name
        
        # Выбираем самую длинную подстроку (наиболее специфичную)
        best_match = max(matching_models, key=len)
        
        self.logger.debug(f"Автоматический маппинг модели: {model_name} -> {best_match}")
        return best_match

    def load_pricing_data(self) -> dict[str, dict[str, float]]:
        """Загружает данные о ценах на API из файла prices.json
        
        Ожидаемый формат файла:
        [
            {
                "model": "gpt-4o-mini",
                "input": 0.60,    # цена за 1M входных токенов в USD
                "output": 2.40    # цена за 1M выходных токенов в USD  
            }
        ]
        """
        try:
            with open(self.price_path, "r", encoding="utf-8") as f:
                prices_list = json.load(f)

            # Преобразуем в словарь для удобного доступа
            pricing_dict = {}
            for price_info in prices_list:
                pricing_dict[price_info["model"]] = {
                    "input": price_info["input"],
                    "output": price_info["output"],
                }

            self.logger.debug(f"Загружены цены для моделей: {list(pricing_dict.keys())}")
            return pricing_dict

        except Exception as e:
            self.logger.warning(f"Не удалось загрузить цены из {self.price_path}: {e}")
            return {}

    def estimate_tokens(self, text: str) -> int:
        """Оценивает количество токенов в тексте"""
        try:
            import tiktoken

            # Определяем нужную кодировку для модели
            if "gpt-4" in self.model_name.lower():
                encoding = tiktoken.encoding_for_model("gpt-4")
            elif "gpt-3.5" in self.model_name.lower():
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            else:
                # Используем cl100k_base как дефолтную кодировку для современных моделей
                encoding = tiktoken.get_encoding("cl100k_base")

            return len(encoding.encode(text))

        except ImportError:
            self.logger.warning(
                "tiktoken не установлен, используем примерную оценку токенов"
            )
            # Примерная оценка: ~4 символа на токен для английского текста
            return len(text) // 4
        except Exception as e:
            self.logger.warning(f"Ошибка при подсчете токенов: {e}")
            return len(text) // 4

    def estimate_cost_per_request(
        self, sample_prompt: str, estimated_output_tokens: int = 100
    ) -> float:
        """Оценивает стоимость одного запроса к API"""
        # Маппим название модели к базовому названию
        mapped_model_name = self.map_model_name(self.model_name)
        
        if mapped_model_name not in self.pricing_data:
            self.logger.error(f"Цена для модели {mapped_model_name} (оригинал: {self.model_name}) не найдена")
            raise ValueError(f"Цена для модели {mapped_model_name} (оригинал: {self.model_name}) не найдена")

        input_tokens = self.estimate_tokens(sample_prompt)
        pricing = self.pricing_data[mapped_model_name]

        # Цены указаны за 1M токенов
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (estimated_output_tokens / 1_000_000) * pricing["output"]

        total_cost = input_cost + output_cost

        self.logger.debug(
            f"Оценка стоимости для {self.model_name} (маппинг: {mapped_model_name}): "
            f"{input_tokens} input токенов (${input_cost:.6f}) + "
            f"{estimated_output_tokens} output токенов (${output_cost:.6f}) = ${total_cost:.6f}"
        )

        return total_cost

    def estimate_total_cost(
        self,
        sample_prompt: str,
        num_requests: int,
        estimated_output_tokens: int = 100,
        include_quality_evaluation: bool = True,
    ) -> dict[str, float]:
        """Оценивает общую стоимость генерации"""
        cost_per_request = self.estimate_cost_per_request(
            sample_prompt, estimated_output_tokens
        )
        total_cost = cost_per_request * num_requests

        # Добавляем стоимость оценки качества (если используется)
        quality_cost_per_request = 0.0
        if include_quality_evaluation:
            # Примерная оценка для quality evaluation
            quality_sample = f"Rate question: {sample_prompt[:100]}... Answer: test"
            quality_cost_per_request = self.estimate_cost_per_request(
                quality_sample, 20
            )

        total_quality_cost = quality_cost_per_request * num_requests
        final_total = total_cost + total_quality_cost

        return {
            "generation_cost": total_cost,
            "quality_evaluation_cost": total_quality_cost,
            "total_cost": final_total,
            "cost_per_request": cost_per_request,
            "quality_cost_per_request": quality_cost_per_request,
        }

    def request_cost_confirmation(
        self,
        sample_prompt: str,
        num_requests: int,
        estimated_output_tokens: int = 100,
        include_quality_evaluation: bool = True,
    ) -> bool:
        """Запрашивает подтверждение пользователя на расходы"""
        cost_breakdown = self.estimate_total_cost(
            sample_prompt, num_requests, estimated_output_tokens, include_quality_evaluation
        )

        print("\n" + "=" * 60)
        print("💰 ОЦЕНКА СТОИМОСТИ API ЗАПРОСОВ")
        print("=" * 60)
        print(f"📝 Примерный промпт: {sample_prompt}...")
        print(f"📊 Модель: {self.model_name}")
        print(f"🔢 Количество запросов: {num_requests:,}")
        print(f"📏 Входных токенов на запрос: ~{self.estimate_tokens(sample_prompt)}")
        print(f"📤 Выходных токенов на запрос: ~{estimated_output_tokens}")
        print("\n💸 РАСЧЕТ СТОИМОСТИ:")
        print(f"   • Генерация вопросов: ${cost_breakdown['generation_cost']:.6f}")
        if include_quality_evaluation:
            print(f"   • Оценка качества: ${cost_breakdown['quality_evaluation_cost']:.6f}")
        print("-" * 40)
        print(f"🚨 ОБЩАЯ СТОИМОСТЬ: ${cost_breakdown['total_cost']:.6f} USD")
        print("=" * 60)

        # Выделяем большие суммы
        if cost_breakdown["total_cost"] > 10.0:
            print("⚠️  ВНИМАНИЕ: Стоимость превышает $10!")
        elif cost_breakdown["total_cost"] > 1.0:
            print("⚠️  ВНИМАНИЕ: Стоимость превышает $1!")

        print("\nПродолжить выполнение? (yes/no): ", end="")
        try:
            response = input().strip().lower()
            return response in ["yes", "y", "да", "д"]
        except KeyboardInterrupt:
            print("\n❌ Операция отменена пользователем")
            return False

    def create_fallback_confirmation(self, error_message: str | None = None) -> bool:
        """Создает запрос подтверждения в случае ошибки оценки стоимости"""
        if error_message:
            print(f"\n⚠️ {error_message}")
        else:
            print("\n⚠️ Не удалось оценить стоимость.")
        print("Продолжить выполнение? (yes/no): ", end="")
        try:
            response = input().strip().lower()
            return response in ["yes", "y", "да", "д"]
        except KeyboardInterrupt:
            print("\n❌ Операция отменена пользователем")
            return False 