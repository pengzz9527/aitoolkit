#!/usr/bin/env python3
import json, urllib.request, urllib.error

# Get HN top stories
ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
ids_resp = urllib.request.urlopen(ids_url, timeout=15)
ids = json.loads(ids_resp.read())

# Get top 30 stories details
stories = []
for sid in ids[:30]:
    try:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        story_resp = urllib.request.urlopen(story_url, timeout=10)
        story = json.loads(story_resp.read())
        if story.get('type') == 'story':
            stories.append(story)
    except:
        pass

for s in stories[:25]:
    title = s.get('title', '')
    url = s.get('url', '') or ''
    points = s.get('points', 0)
    print(f"[{points}] {title} | {url}")
