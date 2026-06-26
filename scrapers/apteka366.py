from typing import List, Dict
from .fetch import fetch

def search_apteka366(query: str) -> List[Dict]:
    resp = fetch("https://apteka.ru/search/?q=" + query.replace(" ", "+"), timeout=5)
    if not resp or resp.status_code != 200:
        return [{"name": query, "price": 0, "url": "https://apteka.ru/search/?q=" + query.replace(" ", "+"), "store": "Аптека.ру"}]

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for card in soup.find_all("div", class_="product-card")[:5]:
        try:
            name_el = card.find("a", class_="product-card__name")
            price_el = card.find("span", class_="price")
            link_el = card.find("a", href=True)
            if name_el and price_el:
                name = name_el.get_text(strip=True)
                price_text = price_el.get_text(strip=True).replace(" ", "").replace("₽", "")
                price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                href = link_el["href"] if link_el else ""
                url = "https://apteka.ru" + href if href and not href.startswith("http") else href
                results.append({"name": name, "price": price, "url": url, "store": "Аптека.ру"})
        except (ValueError, AttributeError):
            continue

    if not results:
        results.append({"name": query, "price": 0, "url": "https://apteka.ru/search/?q=" + query.replace(" ", "+"), "store": "Аптека.ру"})
    return results
