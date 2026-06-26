from playwright.sync_api import sync_playwright
from typing import List, Dict
import time

_browser = None
_context = None

def _get_browser():
    global _browser, _context
    if _browser is None:
        pw = sync_playwright().start()
        _browser = pw.chromium.launch(headless=True)
        _context = _browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="ru-RU",
            timezone_id="Europe/Moscow"
        )
    return _context

def search_wildberries_browser(query: str) -> List[Dict]:
    results = []
    ctx = _get_browser()
    page = ctx.new_page()
    try:
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        cards = page.query_selector_all("article.product-card")
        if not cards:
            cards = page.query_selector_all("[data-nm-id]")

        for card in cards[:5]:
            try:
                name_el = card.query_selector(".product-card__name") or card.query_selector("a span")
                price_el = card.query_selector(".price__lower-price") or card.query_selector("[data-price]")
                link_el = card.query_selector("a[href]")

                if name_el and price_el:
                    name = name_el.inner_text().strip()
                    price_text = price_el.inner_text().strip().replace(" ", "").replace("₽", "")
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    href = link_el.get_attribute("href") if link_el else ""
                    product_url = f"https://www.wildberries.ru{href}" if href and not href.startswith("http") else href

                    if price > 0:
                        results.append({
                            "name": name[:100],
                            "price": price,
                            "url": product_url,
                            "store": "Wildberries"
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"Wildberries browser error: {e}")
    finally:
        page.close()
    return results

def search_ozon_browser(query: str) -> List[Dict]:
    results = []
    ctx = _get_browser()
    page = ctx.new_page()
    try:
        url = f"https://www.ozon.ru/search/?text={query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        cards = page.query_selector_all("[data-widget='searchResultsV2'] .widget-search-result-container")
        if not cards:
            cards = page.query_selector_all("div[data-index]")

        for card in cards[:5]:
            try:
                name_el = card.query_selector("span[class*='tsBody500Medium']") or card.query_selector("a span")
                price_el = card.query_selector("span[class*='Headline500Medium']") or card.query_selector("[class*='price']")
                link_el = card.query_selector("a[href]")

                if name_el and price_el:
                    name = name_el.inner_text().strip()
                    price_text = price_el.inner_text().strip().replace(" ", "").replace("₽", "")
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    href = link_el.get_attribute("href") if link_el else ""
                    product_url = f"https://www.ozon.ru{href}" if href and not href.startswith("http") else href

                    if price > 0:
                        results.append({
                            "name": name[:100],
                            "price": price,
                            "url": product_url,
                            "store": "Ozon"
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"Ozon browser error: {e}")
    finally:
        page.close()
    return results

def search_goldapple_browser(query: str) -> List[Dict]:
    results = []
    ctx = _get_browser()
    page = ctx.new_page()
    try:
        url = f"https://goldapple.ru/search?q={query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)

        cards = page.query_selector_all("[class*='product-card']") or page.query_selector_all("[data-product-id]")

        for card in cards[:5]:
            try:
                name_el = card.query_selector("[class*='product-card__name']") or card.query_selector("a[class*='name']")
                price_el = card.query_selector("[class*='price']") or card.query_selector("[data-price]")
                link_el = card.query_selector("a[href]")

                if name_el and price_el:
                    name = name_el.inner_text().strip()
                    price_text = price_el.inner_text().strip().replace(" ", "").replace("₽", "")
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    href = link_el.get_attribute("href") if link_el else ""
                    product_url = f"https://goldapple.ru{href}" if href and not href.startswith("http") else href

                    if price > 0:
                        results.append({
                            "name": name[:100],
                            "price": price,
                            "url": product_url,
                            "store": "Золотое Яблоко"
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"Goldapple browser error: {e}")
    finally:
        page.close()
    return results

def search_letual_browser(query: str) -> List[Dict]:
    results = []
    ctx = _get_browser()
    page = ctx.new_page()
    try:
        url = f"https://www.letual.ru/search?q={query}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        cards = page.query_selector_all("[class*='product-card']") or page.query_selector_all("[data-product-id]")

        for card in cards[:5]:
            try:
                name_el = card.query_selector("[class*='product-card__name']") or card.query_selector("a[class*='name']")
                price_el = card.query_selector("[class*='price']") or card.query_selector("[data-price]")
                link_el = card.query_selector("a[href]")

                if name_el and price_el:
                    name = name_el.inner_text().strip()
                    price_text = price_el.inner_text().strip().replace(" ", "").replace("₽", "")
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    href = link_el.get_attribute("href") if link_el else ""
                    product_url = f"https://www.letual.ru{href}" if href and not href.startswith("http") else href

                    if price > 0:
                        results.append({
                            "name": name[:100],
                            "price": price,
                            "url": product_url,
                            "store": "Летуаль"
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"Letual browser error: {e}")
    finally:
        page.close()
    return results

def close_browser():
    global _browser, _context
    if _browser:
        _browser.close()
        _browser = None
        _context = None
