from playwright.sync_api import sync_playwright
import time
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pw = sync_playwright().start()
browser = pw.chromium.launch(
    headless=True,
    args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
    ]
)

ctx = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    locale="ru-RU",
    timezone_id="Europe/Moscow",
    viewport={"width": 1920, "height": 1080},
)

# Remove webdriver property
ctx.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en']});
    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
""")

stores = [
    ("Wildberries", "https://www.wildberries.ru/catalog/0/search.aspx?search=Dove"),
    ("Ozon", "https://www.ozon.ru/search/?text=Dove"),
    ("Goldapple", "https://goldapple.ru/search?q=Dove"),
]

for name, url in stores:
    print(f"\n=== {name} ===")
    page = ctx.new_page()
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=45000)
        print(f"Status: {resp.status if resp else 'None'}")

        # Wait more for JS to execute
        time.sleep(8)

        title = page.title()
        print(f"Title: {title}")

        html = page.content()
        print(f"HTML length: {len(html)}")

        # Check for product elements
        all_elements = page.query_selector_all("*")
        print(f"Total elements: {len(all_elements)}")

        # Look for price-like elements
        price_elements = page.query_selector_all("[class*='price'], [class*='Price'], [data-price]")
        print(f"Price elements: {len(price_elements)}")

        # Look for product cards
        card_selectors = [
            "[class*='product-card']",
            "[class*='ProductCard']",
            "[data-product-id]",
            "[data-nm-id]",
            "[data-widget*='search']",
            "article",
        ]
        for sel in card_selectors:
            els = page.query_selector_all(sel)
            if els:
                print(f"  {sel}: {len(els)} elements")
                if len(els) > 0:
                    first = els[0]
                    text = first.inner_text()[:200] if first else ''
                    print(f"    First: {text}")

        # Save HTML for debugging
        with open(f"debug_pw_{name.lower()}.html", "w", encoding="utf-8") as f:
            f.write(html)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        page.close()

browser.close()
pw.stop()
