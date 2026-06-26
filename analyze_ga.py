import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('ga_homepage.html', 'r', encoding='utf-8') as f:
    html = f.read()
print(f'HTML length: {len(html)}')

patterns = ['search', 'poisk', 'query']
for p in patterns:
    count = html.lower().count(p)
    print(f'Pattern "{p}": {count} occurrences')

inputs = re.findall(r'<input[^>]*>', html[:200000])
print(f'Input tags in HTML: {len(inputs)}')
for inp in inputs[:5]:
    print(f'  {inp[:120]}')
