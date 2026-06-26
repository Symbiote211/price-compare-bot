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


def search_goldapple(query: str) -> List[Dict]:
    results = []

    # Try Goldapple search page
    try:
        session = _get_session()
        url = 'https://goldapple.ru/search?q=' + query.replace(' ', '+')
        resp = session.get(url, timeout=10, allow_redirects=True)

        if resp.status_code == 200:
            text = resp.text

            # Check if it's a challenge page
            if 'checking device' in text.lower():
                # Challenge page - try to extract from __NEXT_DATA__
                import re
                next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', text)
                if next_data_match:
                    try:
                        data = json.loads(next_data_match.group(1))
                        props = data.get('props', {}).get('pageProps', {})
                        search_results = props.get('searchResults', [])
                        for item in search_results[:5]:
                            name = item.get('name', '')
                            price = item.get('price', 0)
                            item_id = item.get('id', 0)
                            if name and price:
                                results.append({
                                    'name': name,
                                    'price': float(price),
                                    'url': 'https://goldapple.ru/' + str(item_id),
                                    'store': 'Золотое Яблоко'
                                })
                    except (json.JSONDecodeError, KeyError):
                        pass
    except Exception:
        pass

    # Fallback to search link
    if not results:
        results.append({
            'name': query,
            'price': 0,
            'url': 'https://goldapple.ru/search?q=' + query.replace(' ', '+'),
            'store': 'Золотое Яблоко'
        })

    return results
