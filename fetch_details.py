#!/usr/bin/env python3
import urllib.request, re, sys

articles = [
    ('https://blog.modelcontextprotocol.io/posts/mcp-roadmap/', 'MCP Roadmap'),
    ('https://quantumi.sh/public/labs.html', 'ElevenLabs Labs'),
    ('https://munderdiffl.in/', 'Munder Difflin'),
    ('https://allaboutcoding.ghinda.com/a-week-of-using-codex-more-than-claude/', 'Codex vs Claude'),
    ('https://www.lambda-symbolics.com/autolith', 'Autolith'),
    ('https://forum.level1techs.com/t/why-your-local-llm-feels-dumber-than-it-is/253917', 'Local LLM'),
    ('https://ozbrain.com', 'OzBrain'),
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
        if not snippet_m:
            snippet_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ''
        snippet = snippet_m.group(1).strip() if snippet_m else ''
        print(f"=== {label} ===")
        print(f"Title: {title[:150]}")
        print(f"Snippet: {snippet[:250]}")
        print()
    except Exception as e:
        print(f"Error {label}: {e}")
        print()
