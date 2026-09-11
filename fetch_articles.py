#!/usr/bin/env python3
import json, urllib.request, sys, re

# Fetch more TechCrunch articles for detail
articles = [
    ("OpenAI Pro on hold", "https://techcrunch.com/2026/09/10/openai-puts-pro-subscriptions-on-hold-due-to-astra-demand/"),
    ("Anthropic distillation", "https://techcrunch.com/2026/09/10/anthropic-details-distillation-campaigns-from-alibaba-moonshot-ai-and-deepseek/"),
    ("Meta Muse #2 app", "https://techcrunch.com/2026/09/10/metas-ai-agent-muse-is-now-the-no-2-app-in-the-us/"),
    ("Anthropic CAPTCHA", "https://techcrunch.com/2026/09/10/anthropic-reveals-rogue-ai-agents-hate-captchas-just-like-you/"),
    ("Pocket FM $500M", "https://techcrunch.com/2026/09/10/indias-pocket-fm-doubles-revenue-run-rate-to-500m-as-ai-powers-93-of-audio-content/"),
    ("Listen Labs funding", "https://techcrunch.com/2026/09/09/ai-research-startup-listen-labs-scrubbed-a-1-5b-funding-round-for-salesforce-talks/"),
    ("Nvidia 70% growth", "https://techcrunch.com/2026/09/10/jensen-huang-explains-why-nvidia-will-grow-an-astounding-70-next-year/"),
]

for name, url in articles:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
        # Extract title and first paragraph
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        p_match = re.search(r'<p[^>]*>([^<]+)</p>', content)
        title = (title_match.group(1) if title_match else '') or (h1_match.group(1) if h1_match else name)
        para = p_match.group(1) if p_match else ''
        print(f"\n=== {name} ===")
        print(f"Title: {title[:150]}")
        print(f"Excerpt: {para[:300]}")
    except Exception as e:
        print(f"Error fetching {name}: {e}", file=sys.stderr)
