from typing import List, Dict
from .fetch import fetch

def search_svyetofor(query: str) -> List[Dict]:
    url = "https://svyetofor.ru/search?q=" + query.replace(" ", "+")
    return [{"name": query, "price": 0, "url": url, "store": "Светофор"}]
