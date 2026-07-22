import json, urllib.request, sys

ids = [48979269, 48981703, 48982681, 48982535, 48981206, 48975665, 48980019, 48980053, 48979120, 48981136]

for sid in ids:
    url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    try:
        with urllib.request.urlopen(url) as resp:
            item = json.load(resp)
            if item:
                title = item.get('title', '')
                text = item.get('text', '') or ''
                by = item.get('by', '')
                score = item.get('score', 0)
                kids = len(item.get('children', []))
                print(f"=== ID:{sid} SCORE:{score} BY:{by} COMMENTS:{kids} ===")
                print(f"TITLE: {title}")
                # Strip HTML tags from text
                import re
                clean = re.sub('<[^<]+?>', ' ', text)
                clean = re.sub(r'\s+', ' ', clean).strip()
                print(f"TEXT: {clean[:500]}")
                print()
    except Exception as e:
        print(f"ERROR {sid}: {e}")
