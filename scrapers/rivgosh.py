from typing import List, Dict
from .fetch import fetch

def search_rivgosh(query: str) -> List[Dict]:
    url = "https://rivgosh.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Рив Гош"}]
