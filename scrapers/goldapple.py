from typing import List, Dict
from .fetch import fetch

def search_goldapple(query: str) -> List[Dict]:
    url = "https://goldapple.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Золотое Яблоко"}]
