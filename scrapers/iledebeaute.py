from typing import List, Dict
from .fetch import fetch

def search_iledebeaute(query: str) -> List[Dict]:
    url = "https://iledebeaute.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Иль де Ботэ"}]
