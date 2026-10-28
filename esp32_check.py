import json
from datetime import datetime

commits = json.load(open('/tmp/esp32_commits.json'))
print('recent commits (last 30):')
for c in commits[:30]:
    print(' ', c['commit']['author']['date'], c['commit']['message'].split('\n')[0][:80])

# count commits in last 7 days
now = datetime(2026,10,27)
import datetime as dt
c7 = 0
c30 = 0
for c in commits:
    d = dt.datetime.strptime(c['commit']['author']['date'][:10], '%Y-%m-%d')
    if (now - d).days <= 7: c7 += 1
    if (now - d).days <= 30: c30 += 1
print(f'commits in window (sampled 30): last 7d={c7}, last 30d={c30} (capped at fetched count)')

rels = json.load(open('/tmp/esp32_rel.json'))
print('releases:')
for r in rels:
    print(' ', r.get('tag_name'), r.get('published_at'))
