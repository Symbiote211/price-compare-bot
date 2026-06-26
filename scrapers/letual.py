from typing import List, Dict
from .fetch import fetch

def search_letual(query: str) -> List[Dict]:
    url = "https://www.letual.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Летуаль"}]
