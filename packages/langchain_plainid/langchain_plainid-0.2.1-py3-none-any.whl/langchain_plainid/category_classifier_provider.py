from abc import ABC, abstractmethod
from typing import List, Optional


class CategoryClassifierProvider(ABC):
    @abstractmethod
    def classify(self, input: str, categories: List[str]) -> Optional[str]:
        """
        Classifies the input text and returns the category name.

        Args:
            input (str): The input text to be classified
            categories (List[str]): List of categories to classify input into

        Returns:
            Optional[str]: The classified category name or None if classification failed
        """
