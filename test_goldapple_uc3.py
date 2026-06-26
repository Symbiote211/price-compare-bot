import undetected_chromedriver as uc
import time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--lang=ru-RU')

driver = uc.Chrome(options=options, version_main=149)

# Go to homepage and look at the page
driver.get('https://goldapple.ru/')
time.sleep(10)
print(f'Title: {driver.title}')

# Save the page source
html = driver.page_source
with open('ga_homepage.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Homepage HTML saved ({len(html)} bytes)')

# Look for search-related elements
from selenium.webdriver.common.by import By

inputs = driver.find_elements(By.TAG_NAME, 'input')
print(f'\nInputs found: {len(inputs)}')
for inp in inputs:
    try:
        attrs = {
            'type': inp.get_attribute('type'),
            'name': inp.get_attribute('name'),
            'placeholder': inp.get_attribute('placeholder'),
            'class': inp.get_attribute('class'),
        }
        print(f'  {attrs}')
    except:
        pass

# Look for links with search
links = driver.find_elements(By.TAG_NAME, 'a')
search_links = [l for l in links if 'search' in (l.get_attribute('href') or '').lower() or 'poisk' in (l.get_attribute('href') or '').lower()]
print(f'\nSearch links: {len(search_links)}')
for l in search_links[:5]:
    print(f'  {l.get_attribute("href")}')

driver.quit()
print('Done!')
