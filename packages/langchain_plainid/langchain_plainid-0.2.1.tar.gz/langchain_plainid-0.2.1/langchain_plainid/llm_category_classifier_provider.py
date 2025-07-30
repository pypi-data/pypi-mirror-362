import logging
from typing import List, Optional

from langchain_core.language_models import BaseLLM

from .category_classifier_provider import CategoryClassifierProvider


class LLMCategoryClassifierProvider(CategoryClassifierProvider):
    def __init__(self, llm: BaseLLM):
        """
        Initialize LLMCategoryClassifierProvider with a language model.

        Args:
            llm (BaseLLM): The language model to use for classification
        """
        self.llm = llm

    def classify(self, input: str, categories: List[str]) -> Optional[str]:
        """
        Classifies the input text using the language model.

        Args:
            input (str): The input text to be classified
            categories (List[str]): List of categories to classify input into

        Returns:
            Optional[str]: The classified category name or None if classification failed
        """
        if not categories:
            raise ValueError("Categories list cannot be empty.")

        result = self.llm.invoke(
            f"""You will classify text into one of the provided categories.
                ONLY respond with a single category name from the provided list with best match - no other words, no explanations, no prefix.
                If no category matches, respond with only "None".
                Don't come up with your own categories. If there is no best match, respond with "None".
                If you cannot classify the text's category, respond with "None".
                Text: {input}
                Categories: {categories}
                Response:"""
        )

        logging.debug(
            f"detected category: {result}, list of allowed categories: {categories}"
        )
        result_cleaned = result.strip()
        if result_cleaned.lower() == "none":
            raise ValueError(
                f"No matching category found. Allowed categories: {categories}"
            )

        categories_map = {category.lower(): category for category in categories}

        words = result_cleaned.split()
        for word in reversed(words):
            word_lower = word.lower()
            if word_lower in categories_map:
                return input

        raise ValueError(
            f"No matching category found. Allowed categories: {categories}"
        )
