#!/usr/bin/env python3
import urllib.request, re, sys

articles = [
    ('https://techcrunch.com/2026/08/22/inherent-founded-by-deepmind-alumni-says-its-ai-teammate-just-outperformed-anthropic-and-openai-at-replicating-research/', 'Inherent AI'),
    ('https://techcrunch.com/2026/08/21/starcloud-raises-200-million-for-orbital-data-centers-as-launch-options-dry-up/', 'Starcloud'),
    ('https://techcrunch.com/2026/08/20/ai-data-startup-micro1-reaches-500m-gross-run-rate-amid-ai-training-boom/', 'Micro1'),
]

for url, label in articles:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>(.*?)</title>', html)
        snippet_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if not snippet_m:
            snippet_m = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ''
        snippet = snippet_m.group(1).strip() if snippet_m else ''
        print(f"=== {label} ===")
        print(f"Title: {title[:150]}")
        print(f"Snippet: {snippet[:250]}")
        print()
    except Exception as e:
        print(f"Error {label}: {e}")
        print()
