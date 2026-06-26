import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

query = "Dove"
stores = [
    ("Wildberries", f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}"),
    ("Ozon", f"https://www.ozon.ru/search/?text={query}"),
    ("Яндекс.Маркет", f"https://market.yandex.ru/search?text={query}"),
    ("Золотое Яблоко", f"https://goldapple.ru/search?q={query}"),
    ("Летуаль", f"https://www.letual.ru/search?q={query}"),
    ("Подружка", f"https://www.podruzka.ru/search?text={query}"),
    ("Магнит Косметик", f"https://magnit-cosmetic.ru/search?q={query}"),
    ("Рив Гош", f"https://www.rivgosh.ru/search?q={query}"),
    ("Иль де Ботэ", f"https://iledebeaute.ru/search?q={query}"),
    ("Светофор", f"https://www.svyetofor.ru/search?q={query}"),
    ("Аптека.ру", f"https://apteka.ru/search?q={query}"),
    ("AliExpress", f"https://www.aliexpress.com/wholesale?SearchText={query}"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
}

for name, url in stores:
    try:
        resp = requests.get(url, headers=headers, timeout=8, verify=False, allow_redirects=True)
        final = resp.url
        print(f"{name}: status={resp.status_code} final={final[:80]}")
    except Exception as e:
        print(f"{name}: ERROR - {str(e)[:60]}")
