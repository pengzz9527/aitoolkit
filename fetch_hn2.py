#!/usr/bin/env python3
import urllib.request, re

# Try to get Hacker News RSS for AI-related keywords
# We'll scrape the front page for AI-related items
html = urllib.request.urlopen("https://news.ycombinator.com", timeout=15).read().decode()

# Extract links and scores
items = re.findall(r'<span class="titleline">.*?<a[^>]*href="(\d+)"[^>]*>.*?</a>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', html, re.DOTALL)
scores = re.findall(r'<span class="score">.*?(\d+)\s*points', html)

# Also get the ranking and scores
rank_scores = re.findall(r'<span class="rank">(\d+)</span>.*?<span class="score">(\d+)\s*points</span>.*?<a[^>]*href="[^"]+"[^>]*>([^<]+)</a>', html, re.DOTALL)

for i, (rank, score, title) in enumerate(rank_scores[:20]):
    score_int = int(score)
    if score_int >= 30:
        print(f"{score_int}|{rank}|{title}")
