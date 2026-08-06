#!/usr/bin/env python3
import urllib.request, json

# Get more details on key AI stories
hn_ids = [49161518, 49157930, 49156111, 49156683, 49132992]
for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            print(f"[{data['score']}] {data['title']} | {data.get('url','')[:120]}")
    except Exception as e:
        print(f"Error {sid}: {e}")
