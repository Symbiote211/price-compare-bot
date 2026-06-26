import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
}

url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
params = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'query': 'Dove гель',
    'resultset': 'catalog',
    'spp': '30',
}

resp = requests.get(url, headers=headers, params=params, timeout=15)
data = resp.json()

products = data.get('data', {}).get('products', [])
print(f'Found {len(products)} products\n')

for i, p in enumerate(products[:5]):
    name = p.get('name', '')
    brand = p.get('brand', '')
    id_ = p.get('id', 0)
    sizes = p.get('sizes', [])
    
    price = 0
    sale_price = 0
    if sizes:
        price_info = sizes[0].get('price', {})
        price = price_info.get('total', 0) / 100
        sale_price = price_info.get('total', 0) / 100
    
    link = f'https://www.wildberries.ru/catalog/{id_}/detail.aspx'
    
    print(f'{i+1}. {brand} {name}')
    print(f'   Price: {price} rub')
    print(f'   URL: {link}')
    print()
