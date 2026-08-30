#!/usr/bin/env python3
"""Fetch vLLM and StemDeck details for the daily report."""
import json, urllib.request, re, sys

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

# vLLM release notes
print("=== vLLM v0.28.0 ===")
html = fetch_text("https://github.com/vllm-project/vllm/releases/tag/v0.28.0")
title_match = re.search(r'<title>([^<]+)</title>', html)
if title_match:
    print(f"Title: {title_match.group(1)}")
# Find key changes
changes = re.findall(r'<li>(.*?)</li>', html[:10000], re.DOTALL)
for c in changes[:10]:
    clean = re.sub(r'<[^>]+>', '', c).strip()
    if clean:
        print(f"  - {clean[:120]}")

# StemDeck repo
print("\n=== StemDeck ===")
data = fetch_json("https://api.github.com/repos.stemdeckapp/stemdeck")
print(f"Stars: {data.get('stargazers_count', 0)}")
print(f"Language: {data.get('language', '')}")
print(f"Description: {data.get('description', '')}")
print(f"Created: {data.get('created_at', '')[:10]}")
print(f"Updated: {data.get('updated_at', '')[:10]}")
