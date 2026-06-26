import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
}

# Try different WB API versions
for ver in [3, 4, 5, 6, 7, 8, 9]:
    url = f'https://search.wb.ru/exactmatch/ru/common/v{ver}/search'
    params = {
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'query': 'Dove гель',
        'resultset': 'catalog',
        'spp': '30',
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        text = resp.text[:200] if resp.text else 'EMPTY'
        has_products = 'products' in resp.text
        print(f'v{ver}: status={resp.status_code}, len={len(resp.text)}, has_products={has_products}, preview={text[:80]}')
        if has_products and len(resp.text) > 100:
            data = resp.json()
            products = data.get('data', {}).get('products', [])
            if products:
                print(f'  FOUND {len(products)} products!')
                for p in products[:3]:
                    name = p.get('name', '')
                    brand = p.get('brand', '')
                    prices = p.get('sizes', [])
                    price = 0
                    if prices:
                        price = prices[0].get('price', {}).get('total', 0) / 100
                    print(f'    {brand} {name} - {price} rub')
                break
    except Exception as e:
        print(f'v{ver}: ERROR - {str(e)[:80]}')
