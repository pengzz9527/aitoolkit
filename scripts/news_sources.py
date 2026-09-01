#!/usr/bin/env python3
"""Search for AI industry news using alternative sources"""
import subprocess, re, sys

# Try using a direct web search approach
sources = [
    ("techcrunch", "https://techcrunch.com/category/artificial-intelligence/"),
    ("theverge-ai", "https://www.theverge.com/ai-artificial-intelligence"),
]

for name, url in sources:
    print(f"\n=== {name} ===")
    result = subprocess.run(
        ["curl", "-s", "--max-time", "10", "-H", "User-Agent: Mozilla/5.0", url],
        capture_output=True, text=True
    )
    # Extract article titles and links
    articles = re.findall(r'<a[^>]*href="([^"]*ai[^"]*)"[^>]*>([^<]{20,200})</a>', result.stdout, re.IGNORECASE)
    seen = set()
    for link, title in articles[:8]:
        if "techcrunch.com" in link or "theverge.com" in link:
            if link not in seen:
                seen.add(link)
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                if len(clean_title) > 15:
                    print(f"{clean_title} | {link}")
