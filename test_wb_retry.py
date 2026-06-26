import requests, json, time, sys, io, random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Generate random session
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
]

dest_ids = ['-1257786', '-1029256', '-1257786', '-2133462', '-1029257']

for i in range(3):
    print(f'\nAttempt {i+1}...')
    time.sleep(20)

    ua = random.choice(user_agents)
    dest = random.choice(dest_ids)

    session = requests.Session()
    session.headers.update({
        'User-Agent': ua,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru/catalog/0/search.aspx?search=Dove',
    })

    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params = {
        'appType': '1',
        'curr': 'rub',
        'dest': dest,
        'query': 'Dove гель',
        'resultset': 'catalog',
        'spp': '30',
    }

    try:
        resp = session.get(url, params=params, timeout=15)
        print(f'  Status: {resp.status_code}, Length: {len(resp.text)}')

        if resp.status_code == 200 and len(resp.text) > 1000:
            data = resp.json()
            products = data.get('data', {}).get('products', [])
            print(f'  Products: {len(products)}')
            if products:
                for p in products[:3]:
                    name = p.get('name', '')
                    brand = p.get('brand', '')
                    id_ = p.get('id', 0)
                    sizes = p.get('sizes', [])
                    price = 0
                    if sizes:
                        price = sizes[0].get('price', {}).get('total', 0) / 100
                    print(f'    {brand} {name} - {price} rub')
                break
    except Exception as e:
        print(f'  Error: {e}')
