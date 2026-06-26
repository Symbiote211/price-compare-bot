from typing import List, Dict
from .fetch import fetch

def search_aliexpress(query: str) -> List[Dict]:
    url = "https://aliexpress.ru/popular/" + query.replace(" ", "+") + ".html"
    return [{"name": query, "price": 0, "url": url, "store": "AliExpress"}]
