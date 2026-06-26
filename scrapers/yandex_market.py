from typing import List, Dict
from .fetch import fetch

def search_yandex_market(query: str) -> List[Dict]:
    resp = fetch(f"https://market.yandex.ru/search?text={query}", timeout=5)
    if not resp or resp.status_code != 200:
        return []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for item in soup.find_all("article", {"data-auto": "searchOrganic"})[:5]:
        try:
            name_el = item.find("span", {"data-auto": "snippet-title"})
            price_el = item.find("span", {"data-auto": "snippet-price-current"})
            link_el = item.find("a", {"data-auto": "snippet-link"}, href=True)

            if name_el and price_el:
                name = name_el.get_text(strip=True)
                price_text = price_el.get_text(strip=True).replace(" ", "").replace("₽", "")
                price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                url = "https://market.yandex.ru" + link_el["href"] if link_el else ""

                if price > 0:
                    results.append({"name": name, "price": price, "url": url, "store": "Яндекс.Маркет"})
        except (ValueError, AttributeError):
            continue

    return results
