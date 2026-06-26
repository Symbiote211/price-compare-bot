import undetected_chromedriver as uc
import time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--lang=ru-RU')

driver = uc.Chrome(options=options, version_main=149)

print('Visiting Goldapple...')
driver.get('https://goldapple.ru/')
time.sleep(15)

print(f'Title: {driver.title}')
print(f'URL: {driver.current_url}')

# Try to find any clickable element that looks like search
all_elements = driver.find_elements(By.XPATH, '//*')
print(f'Total elements: {len(all_elements)}')

# Look for elements with search-related attributes
for el in all_elements:
    try:
        attrs = ['data-testid', 'data-auto', 'aria-label', 'placeholder', 'name']
        for attr in attrs:
            val = el.get_attribute(attr)
            if val and ('search' in val.lower() or 'поиск' in val.lower()):
                tag = el.tag_name
                print(f'Found: <{tag}> {attr}="{val}"')
    except:
        pass

# Try keyboard shortcut for search (Ctrl+K or /)
print('\nTrying Ctrl+K...')
from selenium.webdriver.common.action_chains import ActionChains
ActionChains(driver).key_down(Keys.CONTROL).send_keys('k').key_up(Keys.CONTROL).perform()
time.sleep(3)

# Check if search modal appeared
modals = driver.find_elements(By.CSS_SELECTOR, '[class*="modal"], [class*="dialog"], [class*="search"]')
print(f'Modals/dialogs after Ctrl+K: {len(modals)}')

# Try pressing /
ActionChains(driver).send_keys('/').perform()
time.sleep(3)

inputs = driver.find_elements(By.TAG_NAME, 'input')
print(f'Inputs after /: {len(inputs)}')
for inp in inputs:
    try:
        placeholder = inp.get_attribute('placeholder')
        print(f'  Input: placeholder="{placeholder}"')
    except:
        pass

driver.quit()
print('Done!')
