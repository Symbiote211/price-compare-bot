import undetected_chromedriver as uc
import time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--lang=ru-RU')

print('Starting Chrome...')
driver = uc.Chrome(options=options, version_main=149)

print('Visiting Goldapple homepage...')
driver.get('https://goldapple.ru/')
time.sleep(10)
print(f'Title: {driver.title}')
print(f'URL: {driver.current_url}')

print('Searching for Dove...')
driver.get('https://goldapple.ru/search?q=Dove')
time.sleep(10)
print(f'Title: {driver.title}')
print(f'URL: {driver.current_url}')

# Check for products
from selenium.webdriver.common.by import By
cards = driver.find_elements(By.CSS_SELECTOR, '[class*="product"]')
print(f'Product elements: {len(cards)}')

prices = driver.find_elements(By.CSS_SELECTOR, '[class*="price"]')
print(f'Price elements: {len(prices)}')

for el in prices[:5]:
    text = el.text
    if text:
        print(f'  Price: {text[:80]}')

driver.quit()
print('Done!')
