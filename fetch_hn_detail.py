#!/usr/bin/env python3
import json, urllib.request

# Get HN item details for top AI-related stories
item_ids = [49657893, 49651234, 49654321, 49653456, 49655678, 49656789]
# Actually let's search by title
titles_to_find = [
    "Discovery of a new OpenAI agent message board",
    "Formalizing Fermat's Last Theorem",
    "Project HydraFusion",
    "Can AI design circuit boards yet",
    "Next-token predictor is the wrong mental model",
]

# Use Algolia to get full item details
url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50"
with urllib.request.urlopen(url, timeout=15) as resp:
    data = json.loads(resp.read())
for h in data.get("hits", []):
    title = h.get("title", "")
    for keyword in ["OpenAI", "agent", "Anthropic", "Claude", "AI design", "LLM", "multi-model", "Fermat"]:
        if keyword.lower() in title.lower():
            points = h.get("points", 0)
            comments = h.get("num_comments", 0)
            url_h = h.get("url", "") or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
            print(f"HND|{title}|{points}|{comments}|{url_h}")
            break
