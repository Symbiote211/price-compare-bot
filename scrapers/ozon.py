from typing import List, Dict


def search_ozon(query: str) -> List[Dict]:
    encoded = query.replace(" ", "+")
    url = "https://www.ozon.ru/search/?text=" + encoded
    return [{"name": query, "price": 0, "url": url, "store": "Ozon"}]
