import urllib.request
import re

urls = [
    ("https://www.kimi.com/products/kimi-work", "Kimi Work"),
    ("https://news.ycombinator.com/item?id=48979269", "HN China Open Weights"),
    ("https://news.ycombinator.com/item?id=48980019", "HN Kimi K3 Qwen 3.8"),
    ("https://news.ycombinator.com/item?id=48982681", "HN Nativ"),
    ("https://news.ycombinator.com/item?id=48982535", "HN Agent Swarms"),
    ("https://news.ycombinator.com/item?id=48975665", "HN GPT5.6 WordPress RCE"),
]

for url, label in urls:
    print(f"\n=== {label}: {url} ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'})
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        
        if 'hacker-news' in url:
            # Extract comments from HN
            # Find all comment texts
            comments = re.findall(r'<p class="comment"><span class="commit">(.+?)</span></p>', html)
            if not comments:
                # Try another pattern
                texts = re.findall(r'class="commentcode">(.+?)</span>', html)
                if not texts:
                    # Get sitestrings
                    sitestrings = re.findall(r'<span class="sitestr">(.*?)</span>', html, re.DOTALL)
                    for s in sitestrings[:3]:
                        clean = re.sub('<[^<]+?>', '', s).strip()
                        if clean:
                            print(f"SITESTRING: {clean[:300]}")
            else:
                for c in comments[:5]:
                    clean = re.sub('<[^<]+?>', '', c).strip()
                    if clean and len(clean) > 20:
                        print(f"COMMENT: {clean[:300]}")
            
            # Get title
            m = re.search(r'<span class="titleline".*?>(.*?)</span>', html, re.DOTALL)
            if m:
                print(f"HN TITLE: {re.sub('<[^<]+?>', '', m.group(1)).strip()}")
        else:
            # Regular page
            m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
            if m:
                print(f"TITLE: {re.sub('<[^<]+?>', '', m.group(1)).strip()[:200]}")
            m2 = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
            if m2:
                print(f"DESC: {m2.group(1)[:300]}")
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"CONTENT: {text[200:800]}")
    except Exception as e:
        print(f"ERROR: {e}")
