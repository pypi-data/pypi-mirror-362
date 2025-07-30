import logging
from typing import List, Optional

from transformers import pipeline

from .category_classifier_provider import CategoryClassifierProvider

ALL_CATEGORIES = [
    "Weather",
    "Finance",
    "Healthcare",
    "Technology",
    "Education",
    "Sports",
    "Entertainment",
    "Politics",
    "Food",
    "Travel",
    "Fashion",
    "Automotive",
    "Science",
    "Religion",
    "Military",
    "Agriculture",
    "Art",
    "Environment",
    "Law",
    "History",
    "Literature",
    "Mathematics",
    "Architecture",
    "Psychology",
    "Music",
]


class ZeroShotCategoryClassifierProvider(CategoryClassifierProvider):
    """
    A zero-shot category classifier provider implementation.
    Uses Hugging Face transformers pipeline for classification.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.zeroshot_classifier = pipeline(
            "zero-shot-classification", model=model_name
        )

    def classify(self, input: str, categories: List[str]) -> Optional[str]:
        """
        Classifies the input text using zero-shot classification.

        Args:
            input (str): The input text to be classified
            categories (List[str]): List of categories to classify input into

        Returns:
            Optional[str]: The classified category name or None if classification failed
        """
        if not categories:
            raise ValueError("Categories list cannot be empty")

        # Convert categories to lowercase for case-insensitive deduplication
        all_categories_lower = [c.lower() for c in ALL_CATEGORIES]
        input_categories_lower = [c.lower() for c in categories]
        merged_categories = list(set(all_categories_lower + input_categories_lower))

        result = self.zeroshot_classifier(input, merged_categories, multi_label=False)
        top_category = result["labels"][0]

        categories_map = {category.lower(): category for category in categories}

        top_category_lower = top_category.lower()
        if top_category_lower in categories_map:
            matched_category = categories_map[top_category_lower]
            logging.debug(
                f"Classified '{input}' as '{matched_category}' with score {result['scores'][0]}"
            )
            return input

        raise ValueError(
            f"Top category '{top_category}' not in allowed categories: {categories}"
        )

