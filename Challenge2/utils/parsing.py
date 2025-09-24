import re
from typing import Set


COMMON_UNITS = {"cup", "cups", "tbsp", "tablespoon", "tsp", "teaspoon", "grams", "g", "kg", "ml", "l", "oz"}

def normalize(word: str) -> str:
    """Normalize ingredients (remove units, lowercase, singularize simple plurals)"""
    word = word.lower().strip()
    if word.endswith('s') and word[:-1] not in COMMON_UNITS:
        word = word[:-1]
    return word

def parse_ingredients(raw_ingredients: str) -> Set[str]:
    tokens = re.findall(r'\b[a-zA-Z]+\b', raw_ingredients.lower())
    filtered = [normalize(word) for word in tokens if word not in COMMON_UNITS]
    return set(filtered)