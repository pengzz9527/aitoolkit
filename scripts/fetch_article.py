import urllib.request
import re

urls = [
    "https://werd.io/american-ai-is-locked-down-and-proprietary-its-losing/",
    "https://blaizzy.github.io/nativ/",
    "https://cursor.com/blog/agent-swarm-model-economics",
    "https://unslop.run/blog/measuring-ai-writing-on-arxiv",
    "https://www.emergingtrajectories.com/lh/frontier-lab-economics/",
]

for url in urls:
    print(f"=== {url} ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        # Get title
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
        if m:
            print(f"TITLE: {re.sub('<[^<]+?>', '', m.group(1)).strip()}")
        # Get meta description
        m2 = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if m2:
            print(f"DESC: {m2.group(1)[:300]}")
        # Get first meaningful paragraph
        text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Find first 400 chars after title
        print(f"CONTENT: {text[:600]}")
    except Exception as e:
        print(f"ERROR: {e}")
    print()
