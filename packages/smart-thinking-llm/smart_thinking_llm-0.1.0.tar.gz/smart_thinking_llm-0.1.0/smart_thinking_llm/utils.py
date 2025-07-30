import logging
import multiprocessing
import sys

import openai


def init_basic_logger(
    name: str, level: int, with_tqdm: bool = False, file_handler: bool = False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if len(logger.handlers) == 0 and not with_tqdm:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(
            logging.Formatter(fmt="[%(asctime)s: %(levelname)s %(name)s] %(message)s")
        )
        logger.addHandler(handler)
    if file_handler:
        handler = logging.FileHandler(name + ".log")
        handler.setFormatter(
            logging.Formatter(fmt="[%(asctime)s: %(levelname)s %(name)s] %(message)s")
        )
        logger.addHandler(handler)
    return logger

class QuestionQualityMetric():
    def __init__(self, openai_client: openai.OpenAI, openai_model_name: str):
        self.openai_client = openai_client
        self.openai_model_name = openai_model_name
        self.name = "Question Quality Metric"
        self.description = "Measures the quality and naturalness of generated questions"

    def measure(self, question: str, answer: str) -> float:
        # Define evaluation prompt for the LLM to score the question
        eval_prompt = f"""
        Rate the following question (with providedd answer) on a scale from 0 to 1, where:
        - 0 means poor quality: unnatural, confusing, grammatically incorrect
        - 1 means excellent quality: natural, clear, grammatically correct
        
        Question: {question}
        Question answer: {answer}

        Provide only score in the range [0, 1].

        Example 1:
        Question: What is the capital of France?
        Question answer: Paris
        Responce: 1.00

        Example 2:
        Question: What type of institution is Indiana University?
        Question answer: State university system
        Responce: 0.15
        """

        # Call a model to evaluate
        response = self.openai_client.chat.completions.create(
            model=self.openai_model_name,
            messages=[{"role": "user", "content": eval_prompt}],
            max_tokens=16,
            temperature=0.0,
        )
        result = response.choices[0].message.content

        # Extract score
        try:
            score = float(result.strip()) if result else 0.0
        except (ValueError, TypeError) as e:
            print(f"Error occured while parsing score {e}")
            score = 0.0

        return score
    
# Автоматическое определение числа потоков на основе CPU
def get_optimal_threads():
    # Получаем количество логических ядер
    cpu_count = multiprocessing.cpu_count()
    
    # Консервативная оценка
    if cpu_count <= 2:
        return 4
    elif cpu_count <= 4:
        return 8
    else:
        return min(cpu_count * 2, 20)  # Не более 20 потоков

def make_openai_request(openai_client: openai.OpenAI, model_name: str, prompt: str, logger: logging.Logger) -> str:
    """Делает запрос к OpenAI API"""
    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return ""