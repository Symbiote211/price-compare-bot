import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from scrapers.wildberries import search_wildberries
from scrapers.ozon import search_ozon
from scrapers.goldapple import search_goldapple
from scrapers.yandex_market import search_yandex_market

query = 'Dove гель'

print('=== Wildberries ===')
results = search_wildberries(query)
for r in results:
    name = r['name'][:50]
    price = r['price']
    url = r['url'][:60]
    print(f'  {name} - {price} rub - {url}')

print()
print('=== Ozon ===')
results = search_ozon(query)
for r in results:
    name = r['name'][:50]
    price = r['price']
    url = r['url'][:60]
    print(f'  {name} - {price} rub - {url}')

print()
print('=== Goldapple ===')
results = search_goldapple(query)
for r in results:
    name = r['name'][:50]
    price = r['price']
    url = r['url'][:60]
    print(f'  {name} - {price} rub - {url}')

print()
print('=== Yandex Market ===')
results = search_yandex_market(query)
for r in results[:3]:
    name = r['name'][:50]
    price = r['price']
    print(f'  {name} - {price} rub')
