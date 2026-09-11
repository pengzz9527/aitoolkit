#!/usr/bin/env python3
import urllib.request, ssl

ctx = ssl.create_default_context()
headers = {"User-Agent": "Mozilla/5.0"}

# Get more details from docs
urls = [
    "https://docs.browser-use.com/",
    "https://docs.browser-use.com/quickstart",
]
for url in urls:
    print(f"\n=== {url} ===")
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode(errors="ignore")
        # Extract text content
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:1500])
    except Exception as e:
        print(f"Error: {e}")
