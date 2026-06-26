from typing import List, Dict
from .fetch import fetch

def search_magnit_cosmetic(query: str) -> List[Dict]:
    url = "https://magnit-cosmetic.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Магнит Косметик"}]
