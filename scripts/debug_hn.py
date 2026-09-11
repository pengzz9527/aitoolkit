#!/usr/bin/env python3
"""Debug: check what HN API actually returns."""
import json, urllib.request, urllib.parse, time
from datetime import datetime, timezone

# Check what the front_page search returns
url = "https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=5"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

print(f"Front page hits: {len(data.get('hits', []))}")
print(f"Request timestamp: {datetime.now(timezone.utc).isoformat()}")
for h in data.get("hits", []):
    created = h.get("created_at_i", 0)
    age_h = (time.time() - created) / 3600
    print(f"  {h.get('title','')[:60]} | created={created} | age={age_h:.1f}h | pts={h.get('points',0)}")

# Try with date range filter
print("\n--- Trying with dateRange ---")
# Algolia supports numericFilters
url2 = "https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=5&numericFilters=created_at_i>1757356800"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req2, timeout=15) as resp:
    data2 = json.loads(resp.read().decode())
print(f"Front page with date filter: {len(data2.get('hits', []))}")
for h in data2.get("hits", []):
    print(f"  {h.get('title','')[:60]} | pts={h.get('points',0)}")

# Calculate today's epoch (2026-09-09 00:00 UTC)
today_utc = datetime(2026, 9, 9, 0, 0, 0, tzinfo=timezone.utc)
today_epoch = int(today_utc.timestamp())
print(f"\nToday epoch (2026-09-09 00:00 UTC): {today_epoch}")

# Try searching with the correct date
url3 = f"https://hn.algolia.com/api/v1/search?query=AI&tags=front_page&page=1&hitsPerPage=10&numericFilters=created_at_i>={today_epoch}"
req3 = urllib.request.Request(url3, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req3, timeout=15) as resp:
    data3 = json.loads(resp.read().decode())
print(f"\nAI front page today: {len(data3.get('hits', []))}")
for h in data3.get("hits", []):
    print(f"  {h.get('title','')[:60]} | pts={h.get('points',0)} | created={h.get('created_at','')}")
