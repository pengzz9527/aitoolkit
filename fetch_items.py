#!/usr/bin/env python3
import json, urllib.request, urllib.parse, re

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# Get the LLM memory post details from HN
print("=== LLM Memory HN item ===")
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/item/49485416.json")
    print(f"Title: {data.get('title','')}")
    print(f"Score: {data.get('score',0)}")
    print(f"URL: {data.get('url','')}")
    print(f"Type: {data.get('type','')}")
except Exception as e:
    print(f"Failed: {e}")

# Get Tencent Hy4 HN item
print("\n=== Tencent Hy4 HN item ===")
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/item/49492632.json")
    print(f"Title: {data.get('title','')}")
    print(f"Score: {data.get('score',0)}")
    print(f"URL: {data.get('url','')}")
except Exception as e:
    print(f"Failed: {e}")

# Get StemDeck HN item
print("\n=== StemDeck HN item ===")
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/item/49486081.json")
    print(f"Title: {data.get('title','')}")
    print(f"Score: {data.get('score',0)}")
    print(f"URL: {data.get('url','')}")
except Exception as e:
    print(f"Failed: {e}")

# Get Samsung PIM HN item
print("\n=== Samsung PIM HN item ===")
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/item/49487341.json")
    print(f"Title: {data.get('title','')}")
    print(f"Score: {data.get('score',0)}")
    print(f"URL: {data.get('url','')}")
except Exception as e:
    print(f"Failed: {e}")

# Get DHS article
print("\n=== DHS HN item ===")
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/item/49492219.json")
    print(f"Title: {data.get('title','')}")
    print(f"Score: {data.get('score',0)}")
    print(f"URL: {data.get('url','')}")
except Exception as e:
    print(f"Failed: {e}")
