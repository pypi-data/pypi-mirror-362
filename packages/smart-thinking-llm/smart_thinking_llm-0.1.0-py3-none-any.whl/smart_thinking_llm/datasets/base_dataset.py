import logging

from smart_thinking_llm.utils import init_basic_logger


class BaseDataset:
    def __init__(self):
        self.logger = init_basic_logger(__class__.__name__, logging.DEBUG)

    def __getitem__(self, indx: int):
        raise NotImplementedError("Implement __getitem__ method in child class")