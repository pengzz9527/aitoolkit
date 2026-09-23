#!/usr/bin/env python3
"""Fetch AI data from multiple sources and generate daily report."""
import json
import urllib.request
import re
import os
from datetime import datetime, timezone, timedelta

BJ = timezone(timedelta(hours=8))
TODAY = datetime.now(BJ)
DATE_STR = TODAY.strftime("%Y-%m-%d")
FULL_DATE = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

# ── 1. HN Front Page ──────────────────────────────────────────────
print("Fetching HN front page...", flush=True)
hn_data = json.loads(fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=25"))
hn_stories = []
for h in hn_data.get("hits", []):
    title = h.get("title", "")
    points = h.get("points", 0)
    url_val = h.get("url", "") or h.get("objectURL", "")
    comments = h.get("num_comments", 0)
    hn_stories.append({"title": title, "points": points, "url": url_val, "comments": comments})
print(f"  Got {len(hn_stories)} stories", flush=True)

# ── 2. HN AI-specific ─────────────────────────────────────────────
print("Fetching HN AI stories...", flush=True)
ai_keywords = [
    "ai","llm","gpt","openai","claude","deepseek","anthropic","gemini",
    "machine learning","neural","transformer","model","agent","robot",
    "inference","quantization","benchmark","chatbot","generative",
    "diffusion","llama","mistral","grok","xai","perplexity","cursor",
    "copilot","sora","prompt","rag","embedding","multimodal",
    "vision","reasoning","mcp","crewai","langchain","openclaw",
    "watermark","provenance","safety","alignment","rlhf","fine-tune",
    "gemma","qwen","claude sonnet","claude opus","o1","o3","grok",
    "coding agent","ai coding","llm agent","foundation model",
]
def is_ai(title, url=""):
    text = f"{title} {url}".lower()
    return any(k in text for k in ai_keywords)

ai_stories = [s for s in hn_stories if is_ai(s["title"], s["url"]) or s["points"] >= 150]
print(f"  AI-filtered: {len(ai_stories)}", flush=True)

# ── 3. GitHub Trending Python ─────────────────────────────────────
print("Fetching GitHub trending...", flush=True)
try:
    html = fetch("https://github.com/trending/python?since=daily").decode("utf-8", errors="replace")
    repo_matches = re.findall(r'<h2[^>]*>\s*<a href="/([^/]+/[^"]+)"', html)
    desc_matches = re.findall(r'<p class="col-9 color-fg-muted my-1">(.*?)</p>', html)
    star_matches = re.findall(r'(\d[\d,]*)\s*stars?', html)
    gh_trending = []
    for i, repo in enumerate(repo_matches[:12]):
        desc = desc_matches[i].strip() if i < len(desc_matches) else ""
        stars = star_matches[i] if i < len(star_matches) else ""
        gh_trending.append({"repo": repo, "description": desc, "stars": stars})
    print(f"  Got {len(gh_trending)} repos", flush=True)
except Exception as e:
    print(f"  GitHub trending error: {e}", flush=True)
    gh_trending = []

# ── 4. GitHub Trending All Languages ──────────────────────────────
print("Fetching GitHub trending all...", flush=True)
try:
    html2 = fetch("https://github.com/trending?since=daily").decode("utf-8", errors="replace")
    repo_matches2 = re.findall(r'<h2[^>]*>\s*<a href="/([^/]+/[^"]+)"', html2)
    desc_matches2 = re.findall(r'<p class="col-9 color-fg-muted my-1">(.*?)</p>', html2)
    star_matches2 = re.findall(r'(\d[\d,]*)\s*stars?', html2)
    gh_trending_all = []
    for i, repo in enumerate(repo_matches2[:12]):
        desc = desc_matches2[i].strip() if i < len(desc_matches2) else ""
        stars = star_matches2[i] if i < len(star_matches2) else ""
        gh_trending_all.append({"repo": repo, "description": desc, "stars": stars})
    print(f"  Got {len(gh_trending_all)} repos", flush=True)
except Exception as e:
    print(f"  GitHub trending all error: {e}", flush=True)
    gh_trending_all = []

# Save raw data
result = {
    "date": DATE_STR,
    "full_date": FULL_DATE,
    "hn": hn_stories,
    "hn_ai": ai_stories,
    "github_python": gh_trending,
    "github_all": gh_trending_all,
    "fetched_at": datetime.now(BJ).isoformat(),
}
with open(f"/root/aitoolkit/daily_data_{DATE_STR}.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"Data saved to daily_data_{DATE_STR}.json", flush=True)

# Print summary for report generation
print("\n=== HN Top Stories ===")
for s in hn_stories[:15]:
    print(f"  [{s['points']}] {s['title']} -> {s['url']}")

print("\n=== HN AI Stories ===")
for s in ai_stories[:15]:
    print(f"  [{s['points']}] {s['title']} -> {s['url']}")

print("\n=== GitHub Trending (Python) ===")
for r in gh_trending[:10]:
    print(f"  {r['repo']} ⭐{r['stars']} - {r['description'][:80]}")

print("\n=== GitHub Trending (All) ===")
for r in gh_trending_all[:10]:
    print(f"  {r['repo']} ⭐{r['stars']} - {r['description'][:80]}")
