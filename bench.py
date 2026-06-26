import time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from scrapers import (
    search_wildberries, search_ozon, search_yandex_market,
    search_goldapple, search_letual, search_podruzka,
    search_magnit_cosmetic, search_rivgosh, search_iledebeaute,
    search_svyetofor, search_apteka366, search_aliexpress
)

query = "Dove гель"
scrapers = [
    ("Wildberries", search_wildberries),
    ("Ozon", search_ozon),
    ("Yandex Market", search_yandex_market),
    ("Goldapple", search_goldapple),
    ("Letual", search_letual),
    ("Podruzka", search_podruzka),
    ("Magnit Cosmetic", search_magnit_cosmetic),
    ("Rivgosh", search_rivgosh),
    ("Iledebeaute", search_iledebeaute),
    ("Svyetofor", search_svyetofor),
    ("Apteka366", search_apteka366),
    ("AliExpress", search_aliexpress),
]

total = 0
for name, func in scrapers:
    t0 = time.time()
    try:
        results = func(query)
        elapsed = time.time() - t0
        total += elapsed
        priced = [r for r in results if r["price"] > 0]
        print(f"{name}: {elapsed:.1f}s, {len(results)} results, {len(priced)} with price")
    except Exception as e:
        elapsed = time.time() - t0
        total += elapsed
        print(f"{name}: {elapsed:.1f}s, ERROR - {str(e)[:60]}")

print(f"\nTotal: {total:.1f}s")
