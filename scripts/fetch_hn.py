#!/usr/bin/env python3
"""Fetch HN top stories and GitHub trending for AI daily report."""
import json
import urllib.request
import sys

# Fetch HN top story IDs
try:
    req = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15)
    top_ids = json.loads(req.read())[:25]
    
    stories = []
    for story_id in top_ids:
        try:
            sreq = urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10)
            story = json.loads(sreq.read())
            if story.get("type") == "story" and story.get("score", 0) > 10:
                stories.append({
                    "id": story["id"],
                    "title": story.get("title", ""),
                    "score": story.get("score", 0),
                    "comments": story.get("descendants", 0),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story['id']}"),
                    "domain": ""
                })
                # Extract domain from URL
                url = story.get("url", "")
                if url:
                    try:
                        from urllib.parse import urlparse
                        story["domain"] = urlparse(url).netloc
                    except:
                        pass
        except Exception as e:
            pass
    
    stories.sort(key=lambda x: x["score"], reverse=True)
    print(json.dumps(stories[:20], ensure_ascii=False, indent=2))
except Exception as e:
    print(f"HN error: {e}", file=sys.stderr)
    print(json.dumps([]))
