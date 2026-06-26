import requests
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
}

# First hit the main page to get cookies
session = requests.Session()
session.headers.update(headers)
session.get('https://www.wildberries.ru/', timeout=10)
time.sleep(3)

# Then search
url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
params = {
    'ab_testing': 'false',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'lang': 'ru',
    'query': 'Dove гель',
    'resultset': 'catalog',
    'spp': '30',
    'suppressSpellcheck': 'false',
}

resp = session.get(url, params=params, timeout=15)
print(f'Status: {resp.status_code}')
print(f'Length: {len(resp.text)}')

if resp.status_code == 200 and len(resp.text) > 500:
    try:
        data = resp.json()
        products = data.get('data', {}).get('products', [])
        print(f'Products: {len(products)}')
        for p in products[:5]:
            name = p.get('name', '')
            brand = p.get('brand', '')
            id_ = p.get('id', 0)
            sizes = p.get('sizes', [])
            price = 0
            if sizes:
                price = sizes[0].get('price', {}).get('total', 0) / 100
            print(f'  {brand} {name} - {price} rub - https://www.wildberries.ru/catalog/{id_}/detail.aspx')
    except Exception as e:
        print(f'JSON error: {e}')
        print(f'Preview: {resp.text[:300]}')
