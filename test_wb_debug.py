import requests, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('Waiting 60 seconds...')
time.sleep(60)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
})

session.get('https://www.wildberries.ru/', timeout=10)
time.sleep(3)

url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
params = {
    'appType': '1', 'curr': 'rub', 'dest': '-1257786',
    'query': 'Dove гель', 'resultset': 'catalog', 'spp': '30',
}

resp = session.get(url, params=params, timeout=15)
print('Status:', resp.status_code, 'Length:', len(resp.text))

if resp.status_code == 200 and len(resp.text) > 1000:
    data = resp.json()

    # Check all top-level keys
    print('Top keys:', list(data.keys()))

    # Check products at root
    products_root = data.get('products', [])
    print('Products at root:', len(products_root))

    # Check data.products
    d = data.get('data', {})
    if isinstance(d, dict):
        products_data = d.get('products', [])
        print('Products in data:', len(products_data))

    # Try to find products anywhere
    all_products = products_root or products_data
    print('Total products:', len(all_products))

    if all_products:
        for p in all_products[:5]:
            name = p.get('name', '')
            brand = p.get('brand', '')
            pid = p.get('id', 0)
            sizes = p.get('sizes', [])
            price = 0
            if sizes:
                price_info = sizes[0].get('price', {})
                price = price_info.get('total', 0) / 100
            print('  ' + brand + ' ' + name + ' - ' + str(price) + ' rub - id=' + str(pid))
    else:
        # Save response for analysis
        with open('wb_debug.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('Saved wb_debug.json for analysis')
        print('First 500 chars:', json.dumps(data, ensure_ascii=False)[:500])
