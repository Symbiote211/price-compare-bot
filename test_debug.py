from playwright.sync_api import sync_playwright
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=True)
ctx = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    locale="ru-RU",
    timezone_id="Europe/Moscow"
)

stores = [
    ("Wildberries", "https://www.wildberries.ru/catalog/0/search.aspx?search=Dove"),
    ("Ozon", "https://www.ozon.ru/search/?text=Dove"),
    ("Goldapple", "https://goldapple.ru/search?q=Dove"),
    ("Letual", "https://www.letual.ru/search?q=Dove"),
]

for name, url in stores:
    print(f"\n=== {name} ===")
    page = ctx.new_page()
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        print(f"Status: {resp.status if resp else 'None'}")
        time.sleep(5)

        title = page.title()
        print(f"Title: {title}")

        html = page.content()
        print(f"HTML length: {len(html)}")

        with open(f"debug_{name.lower()}.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved debug_{name.lower()}.html")

        all_tags = page.query_selector_all("*")
        tags_with_data = []
        for el in all_tags:
            da = el.get_attribute("data-auto")
            if da:
                tags_with_data.append(da)
        print(f"data-auto tags: {tags_with_data[:20]}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        page.close()

browser.close()
pw.stop()
