#!/usr/bin/env python3
import urllib.request, json

# Get HN items with IDs from latest stories
# Looking for news about AI industry
hn_ids = [49161518, 49160437, 49157997, 49162086, 49161801]
for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            print(f"[{data['score']}] {data['title']}")
            print(f"  {data.get('url','')}")
            print()
    except Exception as e:
        pass
