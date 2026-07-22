import json, urllib.request

# Fetch top story IDs from HN
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
with urllib.request.urlopen(url) as resp:
    ids = json.load(resp)[:30]

# Fetch details for each story
for sid in ids:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    try:
        with urllib.request.urlopen(story_url) as story_resp:
            item = json.load(story_resp)
            if item and item.get('type') == 'story':
                title = item.get('title', '')
                url_link = item.get('url', '') or f"https://news.ycombinator.com/item?id={sid}"
                score = item.get('score', 0)
                print(f"{sid}|{score}|{title}|{url_link}")
    except Exception as e:
        pass
