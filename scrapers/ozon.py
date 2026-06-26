import requests
import json
import time
from typing import List, Dict

_session = None

def _get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9',
        })
    return _session


def search_ozon(query: str) -> List[Dict]:
    results = []

    # Try Ozon search page
    try:
        session = _get_session()
        url = 'https://www.ozon.ru/search/?text=' + query.replace(' ', '+')
        resp = session.get(url, timeout=10, allow_redirects=True)

        if resp.status_code == 200:
            text = resp.text

            # Try to extract from JSON embedded in page
            import re
            json_matches = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', text)
            if json_matches:
                try:
                    data = json.loads(json_matches[0])
                    # Navigate the nested structure
                    search_state = data.get('search', {}).get('searchResults', {})
                    items = search_state.get('items', [])
                    for item in items[:5]:
                        title = item.get('title', '')
                        price_val = item.get('price', 0)
                        item_id = item.get('id', 0)
                        if title and price_val:
                            results.append({
                                'name': title,
                                'price': float(price_val),
                                'url': 'https://www.ozon.ru/product/' + str(item_id),
                                'store': 'Ozon'
                            })
                except (json.JSONDecodeError, KeyError):
                    pass

            # Try regex for prices in HTML
            if not results:
                price_pattern = r'"name":"([^"]+)"[^}]*?"price":"?(\d+)"?'
                matches = re.findall(price_pattern, text)
                for name, price in matches[:5]:
                    if int(price) > 0:
                        results.append({
                            'name': name,
                            'price': float(price),
                            'url': url,
                            'store': 'Ozon'
                        })
    except Exception:
        pass

    # Fallback to search link
    if not results:
        results.append({
            'name': query,
            'price': 0,
            'url': 'https://www.ozon.ru/search/?text=' + query.replace(' ', '+'),
            'store': 'Ozon'
        })

    return results
