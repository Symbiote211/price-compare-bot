import requests, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

time.sleep(10)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
})

# Try catalog search
url = 'https://catalog.wb.ru/catalog/market/v2/catalog'
params = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'query': 'Dove гель',
    'resultset': 'catalog',
    'spp': '30',
    'limit': '30',
}

resp = session.get(url, params=params, timeout=15)
print('Catalog API status:', resp.status_code, 'length:', len(resp.text))

if resp.status_code == 200 and len(resp.text) > 500:
    data = resp.json()
    products = data.get('data', {}).get('products', [])
    print('Products:', len(products))
    for p in products[:5]:
        name = p.get('name', '')
        brand = p.get('brand', '')
        pid = p.get('id', 0)
        sizes = p.get('sizes', [])
        price = 0
        if sizes:
            price = sizes[0].get('price', {}).get('total', 0) / 100
        link = 'https://www.wildberries.ru/catalog/' + str(pid) + '/detail.aspx'
        print('  ', brand, name, '-', price, 'rub')
        print('   ', link)
