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

for name, func in scrapers:
    try:
        results = func(query)
        print(f"{name}: {len(results)} results")
        if results:
            print(f"  First: {results[0]}")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
