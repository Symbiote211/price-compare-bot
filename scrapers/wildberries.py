import requests
import json
import time
from typing import List, Dict

_session = None
_last_request_time = 0

def _get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Origin': 'https://www.wildberries.ru',
            'Referer': 'https://www.wildberries.ru/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
        })
        try:
            _session.get('https://www.wildberries.ru/', timeout=10)
            time.sleep(2)
        except Exception:
            pass
    return _session


def search_wildberries(query: str) -> List[Dict]:
    global _last_request_time
    results = []

    # Rate limit: wait at least 20 seconds between requests
    elapsed = time.time() - _last_request_time
    if elapsed < 20:
        time.sleep(20 - elapsed)

    try:
        session = _get_session()
        url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
        params = {
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'query': query,
            'resultset': 'catalog',
            'spp': '30',
        }
        _last_request_time = time.time()
        resp = session.get(url, params=params, timeout=15)

        if resp.status_code == 200 and len(resp.text) > 1000:
            data = resp.json()

            # Products are at root level OR inside data
            products = data.get('products', [])
            if not products and 'data' in data:
                products = data['data'].get('products', [])

            for p in products[:5]:
                name = p.get('name', '')
                brand = p.get('brand', '')
                pid = p.get('id', 0)
                sizes = p.get('sizes', [])
                price = 0
                if sizes:
                    price = sizes[0].get('price', {}).get('total', 0) / 100

                if price > 0:
                    full_name = (brand + ' ' + name).strip()
                    results.append({
                        'name': full_name,
                        'price': price,
                        'url': 'https://www.wildberries.ru/catalog/' + str(pid) + '/detail.aspx',
                        'store': 'Wildberries'
                    })
    except Exception as e:
        print(f'WB error: {e}')

    if not results:
        results.append({
            'name': query,
            'price': 0,
            'url': 'https://www.wildberries.ru/catalog/0/search.aspx?search=' + query.replace(' ', '+'),
            'store': 'Wildberries'
        })

    return results
