#!/usr/bin/env python3
"""Fetch details for top HN AI stories."""
import json
import urllib.request
import sys

story_ids = [49717558, 49704132, 49715947, 49716476, 49713024, 49711544]

for sid in story_ids:
    try:
        req = urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
        story = json.loads(req.read())
        if story.get("type") == "story":
            print(f"ID:{story['id']} | Title:{story.get('title','')} | Score:{story.get('score',0)} | Comments:{story.get('descendants',0)} | URL:{story.get('url','')}")
    except Exception as e:
        print(f"Error fetching {sid}: {e}")
