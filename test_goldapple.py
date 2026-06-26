import requests
from bs4 import BeautifulSoup
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'ru-RU,ru;q=0.9',
}

resp = requests.get('https://goldapple.ru/search?q=Dove', headers=headers, timeout=15)
soup = BeautifulSoup(resp.text, 'html.parser')

title = soup.title.string if soup.title else 'No title'
print(f'Title: {title}')

# Look for JSON data in scripts
for script in soup.find_all('script'):
    text = script.string or ''
    if 'price' in text.lower() and len(text) > 200:
        print(f'\nScript with price data (len={len(text)}):')
        try:
            data = json.loads(text)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        except:
            print(text[:500])
        break

# Check for __NEXT_DATA__ or similar
next_data = soup.find('script', id='__NEXT_DATA__')
if next_data:
    print(f'\n__NEXT_DATA__ found: {next_data.string[:500]}')

# Check all script types
for script in soup.find_all('script'):
    text = script.string or ''
    if len(text) > 500 and ('product' in text.lower() or 'catalog' in text.lower()):
        print(f'\nScript with product data (len={len(text)}):')
        print(text[:500])
        break
