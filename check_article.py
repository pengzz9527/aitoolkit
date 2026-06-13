#!/usr/bin/env python3
import re, glob

with open('content/guides/ai-ppt-guide.md', 'r') as f:
    content = f.read()

body = content.split('---', 2)[2] if content.count('---') >= 3 else content

chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body))
print(f'Chinese characters in body: {chinese_chars}')

titles = []
for fpath in sorted(glob.glob('content/guides/*.md') + glob.glob('content/reviews/*.md')):
    with open(fpath) as f:
        c = f.read()
    m = re.search(r'^title:\s*"(.+)"', c, re.MULTILINE)
    if m:
        titles.append(m.group(1))
print(f'\nAll titles ({len(titles)}):')
for t in titles:
    print(f'  - {t}')
