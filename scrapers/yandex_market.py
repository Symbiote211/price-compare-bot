import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import YANDEX_MARKET_SEARCH_URL, REQUEST_DELAY
import time


def search_yandex_market(query: str) -> List[Dict]:
    results = []
    url = YANDEX_MARKET_SEARCH_URL.format(query=query)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }

    try:
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("article", {"data-auto": "searchOrganic"})

        for item in items[:5]:
            try:
                name_elem = item.find("span", {"data-auto": "snippet-title"})
                price_elem = item.find("span", {"data-auto": "snippet-price-current"})
                link_elem = item.find("a", {"data-auto": "snippet-link"}, href=True)

                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    price = float(''.join(filter(str.isdigit, price_text)))

                    if link_elem:
                        product_url = "https://market.yandex.ru" + link_elem["href"]
                    else:
                        product_url = url

                    results.append({
                        "name": name,
                        "price": price,
                        "url": product_url,
                        "store": "Яндекс.Маркет"
                    })
            except (ValueError, AttributeError):
                continue

    except Exception as e:
        print(f"Yandex Market scraping error: {e}")

    return results
