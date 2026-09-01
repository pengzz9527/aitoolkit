#!/usr/bin/env python3
"""Fetch AI news from specialized sources"""
import json, urllib.request, sys

# Try arXiv API for recent AI papers
url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&start=0&max_results=10&sort=submittedDate&sort_order=descending"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode("utf-8")
    
    import xml.etree.ElementTree as ET
    root = ET.fromstring(content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    print("=== ARXIV AI PAPERS ===")
    for entry in root.findall("atom:entry", ns)[:8]:
        title = entry.find("atom:title", ns).text.replace("\n", " ")[:120]
        link = entry.find("atom:link", ns).get("href", "")
        published = entry.find("atom:published", ns).text[:10]
        print(f"[{published}] {title} | {link}")
except Exception as e:
    print(f"arXiv error: {e}")

# Check LiveKit Agents details
print("\n=== LIVEKIT AGENTS DETAIL ===")
try:
    req = urllib.request.Request("https://api.github.com/repos/livekit/agents", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    print(f"Stars: {data.get('stargazers_count')}")
    print(f"Description: {data.get('description')}")
    print(f"Language: {data.get('language')}")
    print(f"Topics: {data.get('topics')}")
except Exception as e:
    print(f"Error: {e}")
