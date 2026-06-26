import requests, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('Waiting 15 seconds...')
time.sleep(15)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Dove',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
})

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
print(f'Status: {resp.status_code}, Length: {len(resp.text)}')

if resp.status_code == 200 and len(resp.text) > 1000:
    data = resp.json()
    products = data.get('data', {}).get('products', [])
    print(f'Products: {len(products)}')
    if products:
        for p in products[:5]:
            name = p.get('name', '')
            brand = p.get('brand', '')
            id_ = p.get('id', 0)
            sizes = p.get('sizes', [])
            price = 0
            if sizes:
                price = sizes[0].get('price', {}).get('total', 0) / 100
            print(f'  {brand} {name} - {price} rub - id={id_}')
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
else:
    print(f'Failed: {resp.text[:300]}')
