from typing import List, Dict
from .fetch import fetch

def search_podruzka(query: str) -> List[Dict]:
    url = "https://www.podrygka.ru/search/?text=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Подружка"}]
