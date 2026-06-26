import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=True)
ctx = browser.new_context(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    locale='ru-RU',
    timezone_id='Europe/Moscow',
    viewport={'width': 1920, 'height': 1080},
)

page = ctx.new_page()
Stealth().apply_stealth_sync(page)

print('Visiting homepage...')
page.goto('https://goldapple.ru/', wait_until='networkidle', timeout=30000)
time.sleep(8)
print(f'Title: {page.title()}')

print('Searching...')
page.goto('https://goldapple.ru/search?q=Dove', wait_until='networkidle', timeout=30000)
time.sleep(8)
print(f'Title: {page.title()}')
print(f'HTML len: {len(page.content())}')

cards = page.query_selector_all('[class*="product"]')
print(f'Product elements: {len(cards)}')

prices = page.query_selector_all('[class*="price"]')
print(f'Price elements: {len(prices)}')

for el in prices[:5]:
    text = el.inner_text()
    if text:
        print(f'  Price: {text[:50]}')

browser.close()
pw.stop()
print('Done!')
