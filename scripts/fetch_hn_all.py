#!/usr/bin/env python3
import json, os, time
from datetime import datetime, timezone, timedelta

now = time.time()
cutoff = int(now - 48 * 3600)  # Last 48 hours
print(f"Now: {datetime.now(timezone.utc).isoformat()}")
print(f"Cutoff (48h ago): {cutoff}")
print(f"Cutoff date: {datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat()}")

# Re-fetch with relaxed cutoff
import urllib.request
queries = [
    ("hn_ai_front", "AI", "front_page"),
    ("hn_claude", "Claude", "front_page"),
    ("hn_deepseek", "DeepSeek", "front_page"),
    ("hn_gpt", "GPT", "front_page"),
    ("hn_coding_agent", "coding agent", "front_page"),
    ("hn_anthropic", "Anthropic", "front_page"),
    ("hn_openai", "OpenAI", "front_page"),
    ("hn_llm", "large language model", "front_page"),
    ("hn_agent", "AI agent", "front_page"),
]

for fname, query, tag in queries:
    q = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags={tag}&hitsPerPage=10&numericFilters=created_at_i>={cutoff}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        hits = data.get("hits", [])
        with open(f"/root/aitoolkit/scripts/.cache/{fname}.json", "w") as f:
            json.dump(hits, f)
        print(f"  {fname}: {len(hits)} hits")
    except Exception as e:
        print(f"  {fname}: ERROR {e}")
