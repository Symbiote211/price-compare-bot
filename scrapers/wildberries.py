from typing import List, Dict


def search_wildberries(query: str) -> List[Dict]:
    encoded = query.replace(" ", "+")
    url = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + encoded
    return [{"name": query, "price": 0, "url": url, "store": "Wildberries"}]
