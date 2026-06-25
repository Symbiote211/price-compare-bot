import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import OZON_SEARCH_URL, REQUEST_DELAY
import time
import json


def search_ozon(query: str) -> List[Dict]:
    results = []
    url = OZON_SEARCH_URL.format(query=query)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }

    try:
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all("script", type="application/json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                if "searchResult" in str(data)[:100]:
                    items = data.get("widgetStates", {}).get("searchResultsV2", [])
                    if isinstance(items, list):
                        for item in items[:5]:
                            results.append({
                                "name": item.get("title", ""),
                                "price": float(item.get("price", "0").replace(" ", "")),
                                "url": f"https://www.ozon.ru{item.get('link', '')}",
                                "store": "Ozon"
                            })
                    break
            except (json.JSONDecodeError, ValueError):
                continue

        if not results:
            cards = soup.find_all("div", class_="widget-search-result-container")
            for card in cards[:5]:
                name = card.find("span", class_="tsBody500Medium")
                price = card.find("span", class_="tsHeadline500Medium")
                if name and price:
                    results.append({
                        "name": name.get_text(strip=True),
                        "price": float(''.join(filter(str.isdigit, price.get_text()))),
                        "url": url,
                        "store": "Ozon"
                    })

    except Exception as e:
        print(f"Ozon scraping error: {e}")

    return results
