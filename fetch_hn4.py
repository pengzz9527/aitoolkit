#!/usr/bin/env python3
import urllib.request, json, sys

hn_ids = [
    49161518, 49157930, 49156111, 49156683, 49132992,
    49158581, 49156682, 49158474, 49155629, 49156011,
    49160437, 49157997, 49106935, 49161801, 49082937,
    49123105, 49131250, 49124213, 49159676, 49154228
]

for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            print(f"[{data['score']:5d}] {data['title'][:90]} | {data.get('url','')[:100]}")
    except Exception as e:
        pass
