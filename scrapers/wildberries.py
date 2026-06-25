import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import WILDBERRIES_SEARCH_URL, REQUEST_DELAY
import time


def search_wildberries(query: str) -> List[Dict]:
    results = []
    url = WILDBERRIES_SEARCH_URL.format(query=query)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("div", class_="product-card")

        for card in cards[:5]:
            try:
                name_elem = card.find("a", class_="product-card__name")
                price_elem = card.find("span", class_="price")
                link_elem = card.find("a", href=True)

                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    price = float(''.join(filter(str.isdigit, price_text)))
                    product_url = f"https://www.wildberries.ru{link_elem['href']}" if link_elem else ""

                    results.append({
                        "name": name,
                        "price": price,
                        "url": product_url,
                        "store": "Wildberries"
                    })
            except (ValueError, AttributeError):
                continue

    except Exception as e:
        print(f"Wildberries scraping error: {e}")

    return results
