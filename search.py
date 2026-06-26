from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import time

def _safe_search(func, query):
    try:
        return func(query)
    except Exception as e:
        print(f"Scraper error: {e}")
        return []

def search_all_stores(query: str) -> List[Dict]:
    from scrapers.wildberries import search_wildberries
    from scrapers.ozon import search_ozon
    from scrapers.yandex_market import search_yandex_market
    from scrapers.goldapple import search_goldapple
    from scrapers.letual import search_letual
    from scrapers.podruzka import search_podruzka
    from scrapers.magnit_cosmetic import search_magnit_cosmetic
    from scrapers.rivgosh import search_rivgosh
    from scrapers.iledebeaute import search_iledebeaute
    from scrapers.svyetofor import search_svyetofor
    from scrapers.apteka366 import search_apteka366
    from scrapers.aliexpress import search_aliexpress
    all_results = []
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

    total_start = time.time()

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {}
        for name, func in scrapers:
            future = executor.submit(_safe_search, func, query)
            futures[future] = name

        for future in futures:
            try:
                results = future.result(timeout=10)
                all_results.extend(results)
            except FuturesTimeoutError:
                print(f"Timeout: {futures[future]}")
            except Exception as e:
                print(f"Error: {futures[future]} - {e}")

    total_elapsed = time.time() - total_start
    print(f"Search completed in {total_elapsed:.1f}s, {len(all_results)} results")

    all_results.sort(key=lambda x: x.get("price", 0))
    return all_results

def format_results(results: List[Dict]) -> str:
    if not results:
        return "Товары не найдены"

    priced = [r for r in results if r.get("price", 0) > 0]
    links = [r for r in results if r.get("price", 0) == 0]

    lines = []

    if priced:
        priced.sort(key=lambda x: x["price"])
        lines.append("Найдено {} товаров с ценами:\n".format(len(priced)))

        for i, r in enumerate(priced[:10], 1):
            lines.append("{}. {} - {} руб".format(i, r["store"], r["price"]))
            lines.append("   {}".format(r["name"][:60]))
            lines.append("   {}\n".format(r["url"]))

    if links:
        lines.append("\nПосмотреть цены в других магазинах:")
        for r in links:
            lines.append("- {}: {}".format(r["store"], r["url"]))

    if not priced and not links:
        return "Товары не найдены"

    return "\n".join(lines)
