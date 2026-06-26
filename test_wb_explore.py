import requests, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

time.sleep(20)

# Try WB catalog search with different approach
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/',
})

# Warm up
try:
    session.get('https://www.wildberries.ru/', timeout=10)
    time.sleep(3)
except:
    pass

# Try different search endpoints
urls = [
    'https://search.wb.ru/exactmatch/ru/common/v4/search',
    'https://search.wb.ru/exactmatch/ru/common/v7/search',
    'https://search.wb.ru/exactmatch/ru/common/v9/search',
]

params = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'query': 'Dove гель',
    'resultset': 'catalog',
    'spp': '30',
}

for url in urls:
    version = url.split('/')[-2]
    try:
        resp = session.get(url, params=params, timeout=10)
        print(f'{version}: status={resp.status_code}, len={len(resp.text)}')

        if resp.status_code == 200 and len(resp.text) > 1000:
            data = resp.json()

            # Try different product locations
            products = []
            if 'data' in data:
                d = data['data']
                if isinstance(d, dict):
                    products = d.get('products', [])
                    if not products:
                        # Check for other keys
                        for k, v in d.items():
                            if isinstance(v, list) and len(v) > 0:
                                print(f'  Found list in data.{k}: {len(v)} items')
                                if isinstance(v[0], dict):
                                    print(f'  First item keys: {list(v[0].keys())[:10]}')

            print(f'  Products: {len(products)}')
            if products:
                p = products[0]
                print(f'  First product: {json.dumps(p, ensure_ascii=False)[:300]}')
                break
    except Exception as e:
        print(f'{version}: ERROR - {str(e)[:60]}')

    time.sleep(5)
