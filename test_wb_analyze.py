import requests, json, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Dove',
})

url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
params = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'query': 'Dove гель',
    'resultset': 'catalog',
    'spp': '30',
}

resp = session.get(url, params=params, timeout=15)
print(f'Status: {resp.status_code}, Length: {len(resp.text)}')

if resp.status_code == 200 and len(resp.text) > 1000:
    data = resp.json()

    # Save full response
    with open('wb_full_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Explore all keys recursively
    def explore(obj, path='', depth=0):
        if depth > 4:
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f'{path}.{k}' if path else k
                if isinstance(v, list):
                    print(f'{new_path}: list[{len(v)}]')
                    if v and isinstance(v[0], dict):
                        print(f'  first item keys: {list(v[0].keys())[:10]}')
                elif isinstance(v, dict):
                    print(f'{new_path}: dict')
                    explore(v, new_path, depth+1)
                elif isinstance(v, (str, int, float, bool)):
                    val_str = str(v)[:50]
                    print(f'{new_path}: {type(v).__name__} = {val_str}')
        elif isinstance(obj, list):
            print(f'{path}: list[{len(obj)}]')
            if obj and isinstance(obj[0], dict):
                print(f'  first item keys: {list(obj[0].keys())[:10]}')

    explore(data)
