#!/usr/bin/env python3
import json, urllib.request, sys

# Fetch Cognition SWE-2 details
url = "https://cognition.com/blog/swe-2"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read().decode('utf-8', errors='ignore')
    import re
    # Extract some text
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text)
    print(f"Cognition SWE-2 page excerpt: {text[:800]}")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)

# Fetch OpenAI Agents API
url2 = "https://developers.openai.com/api/docs/guides/agents-api/overview"
try:
    req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req2, timeout=15) as r:
        content2 = r.read().decode('utf-8', errors='ignore')
    import re
    text2 = re.sub(r'<[^>]+>', ' ', content2)
    text2 = re.sub(r'\s+', ' ', text2)
    print(f"OpenAI Agents API excerpt: {text2[:800]}")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
