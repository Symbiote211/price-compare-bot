import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=ru-RU')

print("Starting undetected Chrome...")
driver = uc.Chrome(options=options, version_main=137)

try:
    # Test Wildberries
    print("\n=== Wildberries ===")
    driver.get("https://www.wildberries.ru/catalog/0/search.aspx?search=Dove")
    time.sleep(8)
    print(f"Title: {driver.title}")
    print(f"URL: {driver.current_url}")
    
    # Check for products
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, "[data-nm-id]")
        print(f"Product cards: {len(cards)}")
        for card in cards[:3]:
            try:
                name = card.find_element(By.CSS_SELECTOR, "span.product-card__name").text
                price = card.find_element(By.CSS_SELECTOR, "ins.price__lower-price").text
                print(f"  {name[:50]} - {price}")
            except:
                pass
    except Exception as e:
        print(f"Parse error: {e}")

    # Test Ozon
    print("\n=== Ozon ===")
    driver.get("https://www.ozon.ru/search/?text=Dove")
    time.sleep(8)
    print(f"Title: {driver.title}")
    print(f"URL: {driver.current_url}")
    
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, "[data-widget='searchResultsV2'] > div")
        print(f"Product cards: {len(cards)}")
    except Exception as e:
        print(f"Parse error: {e}")

finally:
    driver.quit()
    print("\nDone!")
