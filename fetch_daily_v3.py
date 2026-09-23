#!/usr/bin/env python3
"""Enhanced data fetching for daily AI report."""
import json
import urllib.request
import re
from datetime import datetime, timezone, timedelta

BJ = timezone(timedelta(hours=8))
DATE_STR = datetime.now(BJ).strftime("%Y-%m-%d")
FULL_DATE = datetime.now(BJ).strftime("%B %d, %Y").replace(" 0", " ")

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

result = {"date": DATE_STR, "full_date": FULL_DATE}

# ── 1. HN Front Page ──
print("Fetching HN front page...", flush=True)
hn = json.loads(fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"))
hn_stories = []
for h in hn.get("hits", []):
    hn_stories.append({
        "title": h.get("title", ""),
        "points": h.get("points", 0),
        "url": h.get("url", "") or h.get("objectURL", ""),
        "comments": h.get("num_comments", 0),
    })
result["hn_all"] = hn_stories
print(f"  {len(hn_stories)} stories", flush=True)

# ── 2. AI-filtered HN ──
ai_keywords = [
    "ai","llm","gpt","openai","claude","deepseek","anthropic","gemini",
    "machine learning","neural","transformer","model","agent","robot",
    "inference","quantization","benchmark","chatbot","generative",
    "diffusion","llama","mistral","grok","xai","perplexity","cursor",
    "copilot","sora","prompt","rag","embedding","multimodal",
    "vision","reasoning","mcp","crewai","langchain","openclaw",
    "watermark","provenance","safety","alignment","rlhf","fine-tune",
    "gemma","qwen","o1","o3","agentic","automated reasoning",
    "foundation model","code generation","coding agent",
]
def is_ai(title, url=""):
    text = f"{title} {url}".lower()
    return any(k in text for k in ai_keywords)

hn_ai = [s for s in hn_stories if is_ai(s["title"], s.get("url","")) or s["points"] >= 200]
result["hn_ai"] = hn_ai
print(f"  AI-filtered: {len(hn_ai)}", flush=True)

# ── 3. GitHub Trending via scrape (more reliable) ──
print("Fetching GitHub trending...", flush=True)
gh_repos = []
try:
    html = fetch("https://github.com/trending/python?since=daily").decode("utf-8", errors="replace")
    repo_matches = re.findall(r'<h2[^>]*>\s*<a href="/([^/]+/[^"]+)"', html)
    desc_matches = re.findall(r'<p class="col-9 color-fg-muted my-1">(.*?)</p>', html)
    for i, repo in enumerate(repo_matches[:15]):
        desc = desc_matches[i].strip() if i < len(desc_matches) else ""
        gh_repos.append({"repo": repo, "description": desc})
except Exception as e:
    print(f"  Scrape error: {e}", flush=True)

# Also try JS/other languages for AI repos
try:
    html2 = fetch("https://github.com/trending/javascript?since=daily").decode("utf-8", errors="replace")
    repo_matches2 = re.findall(r'<h2[^>]*>\s*<a href="/([^/]+/[^"]+)"', html2)
    desc_matches2 = re.findall(r'<p class="col-9 color-fg-muted my-1">(.*?)</p>', html2)
    for i, repo in enumerate(repo_matches2[:10]):
        desc = desc_matches2[i].strip() if i < len(desc_matches2) else ""
        if not any(r["repo"] == repo for r in gh_repos):
            gh_repos.append({"repo": repo, "description": desc})
except Exception as e:
    print(f"  JS scrape error: {e}", flush=True)

result["github_trending"] = gh_repos
print(f"  {len(gh_repos)} repos", flush=True)

# ── 4. GitHub search for recently starred AI repos ──
print("Fetching GitHub API for AI repos...", flush=True)
try:
    api_url = "https://api.github.com/search/repositories?q=created:>=2026-09-22&sort=stars&order=desc&per_page=10"
    api_data = json.loads(fetch(api_url))
    for item in api_data.get("items", []):
        name = item["full_name"]
        desc = item.get("description") or ""
        stars = item["stargazers_count"]
        text = f"{name} {desc}".lower()
        if any(k in text for k in ai_keywords):
            existing = [r["repo"] for r in result["github_trending"]]
            if name not in existing:
                result["github_trending"].append({"repo": name, "description": desc, "stars": f"{stars}"})
except Exception as e:
    print(f"  API error: {e}", flush=True)

# ── 5. arXiv recent AI papers ──
print("Fetching arXiv AI papers...", flush=True)
try:
    rss_url = "http://arxiv.org/rss/cs.AI"
    rss = fetch(rss_url).decode("utf-8", errors="replace")
    papers = re.findall(r'<title>([^<]*?)</title>.*?<link>([^<]*?)</link>.*?<description>([^<]*?)</description>', rss, re.DOTALL)
    arxiv_papers = []
    for title, link, desc in papers[:8]:
        title = re.sub(r'\s*\(arXiv:\d+\)', '', title).strip()
        arxiv_papers.append({"title": title, "link": link, "description": desc.strip()[:120]})
    result["arxiv"] = arxiv_papers
    print(f"  {len(arxiv_papers)} papers", flush=True)
except Exception as e:
    print(f"  arXiv error: {e}", flush=True)
    result["arxiv"] = []

# ── 6. HNSearch for specific AI topics ──
print("Fetching additional HN searches...", flush=True)
extra_queries = [
    ("agent", "agent AI"),
    ("coding", "coding AI tool"),
    ("open source model", "open source LLM"),
]
all_extra = []
for query, label in extra_queries:
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=front_page&hitsPerPage=5"
        data = json.loads(fetch(url))
        for h in data.get("hits", []):
            all_extra.append({
                "title": h.get("title", ""),
                "points": h.get("points", 0),
                "url": h.get("url", "") or h.get("objectURL", ""),
            })
    except Exception:
        pass
result["extra_hn"] = all_extra
print(f"  {len(all_extra)} extra stories", flush=True)

# Save
out = f"/root/aitoolkit/daily_data_{DATE_STR}.json"
with open(out, "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"Saved to {out}", flush=True)

# Print summary
print("\n=== AI STORIES ===")
for s in hn_ai[:12]:
    print(f"  [{s['points']}] {s['title']} -> {s['url']}")

print("\n=== GITHUB TRENDING ===")
for r in result["github_trending"][:10]:
    print(f"  {r['repo']} - {r.get('description','')[:60]}")

print("\n=== ARXIV ===")
for p in result.get("arxiv", [])[:5]:
    print(f"  {p['title'][:70]}")

print("\n=== EXTRA HN ===")
for s in all_extra[:5]:
    print(f"  [{s['points']}] {s['title']} -> {s['url']}")
