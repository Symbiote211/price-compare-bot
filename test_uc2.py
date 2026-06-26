import undetected_chromedriver as uc
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--lang=ru-RU')

print("Starting undetected Chrome...")
driver = uc.Chrome(options=options)
ver = driver.capabilities.get("browserVersion", "unknown")
print(f"Chrome version: {ver}")

print("\n=== Wildberries ===")
driver.get("https://www.wildberries.ru/catalog/0/search.aspx?search=Dove")
import time
time.sleep(10)
print(f"Title: {driver.title}")
print(f"URL: {driver.current_url[:100]}")
html = driver.page_source
print(f"HTML length: {len(html)}")

from selenium.webdriver.common.by import By
cards = driver.find_elements(By.CSS_SELECTOR, "[data-nm-id]")
print(f"Product cards with data-nm-id: {len(cards)}")

cards2 = driver.find_elements(By.CSS_SELECTOR, "article")
print(f"Article elements: {len(cards2)}")

# Try broader selectors
all_divs = driver.find_elements(By.CSS_SELECTOR, "div")
print(f"Total divs: {len(all_divs)}")

# Save HTML
with open("debug_uc_wb.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
print("\nDone!")
