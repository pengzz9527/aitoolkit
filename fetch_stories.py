#!/usr/bin/env python3
import urllib.request, json

# Get HN story details
hn_ids = [49157930, 49156111, 49132992, 49158581, 49156682, 49158474, 49155629, 49156011, 49160437, 49157997, 49106935]
for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            print(f"[{data['score']}] {data['title']}")
            print(f"  {data.get('url', '')}")
    except:
        pass
