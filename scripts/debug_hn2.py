#!/usr/bin/env python3
"""Debug: fetch and save HN front page with timestamps."""
import json, urllib.request, time
from datetime import datetime, timezone, timedelta

now = time.time()
# Last 30 hours
cutoff = int(now - 30 * 3600)
print(f"Current UTC time: {datetime.now(timezone.utc).isoformat()}")
print(f"Current +08 time: {datetime.now(timezone(timedelta(hours=8))).isoformat()}")
print(f"Cutoff epoch (30h ago): {cutoff}")

url = "https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=30&numericFilters=created_at_i>={}".format(cutoff)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

hits = data.get("hits", [])
print(f"\nFront page stories (last 30h): {len(hits)}")
for h in hits:
    created = h.get("created_at_i", 0)
    age_h = (now - created) / 3600
    print(f"  [{h.get('points',0)}pts/{h.get('num_comments',0)}c] ({age_h:.1f}h ago) {h.get('title','')[:70]}")

# Save for later use
with open("/root/aitoolkit/scripts/.cache/hn_front_recent.json", "w") as f:
    json.dump(hits, f, indent=2)
print(f"\nSaved {len(hits)} stories to cache")
