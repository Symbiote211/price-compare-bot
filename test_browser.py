from scrapers.browser import search_wildberries_browser, search_ozon_browser, search_goldapple_browser

query = "Dove гель"

print("=== Wildberries ===")
try:
    results = search_wildberries_browser(query)
    print(f"Results: {len(results)}")
    for r in results[:3]:
        print(f"  {r['name'][:60]} - {r['price']} rub")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Ozon ===")
try:
    results = search_ozon_browser(query)
    print(f"Results: {len(results)}")
    for r in results[:3]:
        print(f"  {r['name'][:60]} - {r['price']} rub")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Goldapple ===")
try:
    results = search_goldapple_browser(query)
    print(f"Results: {len(results)}")
    for r in results[:3]:
        print(f"  {r['name'][:60]} - {r['price']} rub")
except Exception as e:
    print(f"Error: {e}")

from scrapers.browser import close_browser
close_browser()
