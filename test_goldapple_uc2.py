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
time.sleep(8)
print(f'Homepage title: {driver.title}')

# Try different search URL formats
urls = [
    'https://goldapple.ru/search?q=Dove',
    'https://goldapple.ru/search?query=Dove',
    'https://goldapple.ru/search?text=Dove',
    'https://goldapple.ru/poisk?q=Dove',
    'https://goldapple.ru/catalogsearch/result/?q=Dove',
]

for url in urls:
    driver.get(url)
    time.sleep(3)
    title = driver.title
    print(f'{url}: title={title[:60]}')

# Try using the search box on the homepage
print('\nTrying search box...')
driver.get('https://goldapple.ru/')
time.sleep(5)

# Look for search input
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

try:
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[type="search"], input[name="q"], input[placeholder*="Поиск"], input[placeholder*="поиск"]')
    print(f'Found search input: {search_input.get_attribute("placeholder")}')
    search_input.clear()
    search_input.send_keys('Dove')
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    print(f'After search: title={driver.title} url={driver.current_url[:80]}')
    
    # Check for products
    cards = driver.find_elements(By.CSS_SELECTOR, '[class*="product"]')
    print(f'Product elements: {len(cards)}')
    
    prices = driver.find_elements(By.CSS_SELECTOR, '[class*="price"]')
    print(f'Price elements: {len(prices)}')
    
    for el in prices[:5]:
        text = el.text
        if text:
            print(f'  Price: {text[:80]}')
except Exception as e:
    print(f'Search box error: {e}')

driver.quit()
print('Done!')
