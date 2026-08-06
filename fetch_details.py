#!/usr/bin/env python3
import urllib.request, json

# Get details for top AI stories
hn_ids = [49157930, 49156111, 49132992, 49158581, 49156682, 49158474]
for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            print(f"[{data['score']}] {data['title']}")
            print(f"  {data.get('url','')}")
            print(f"  by {data.get('by','')} | {data.get('descendants',0)} comments")
            print()
    except Exception as e:
        pass
