#!/usr/bin/env python3
import json, urllib.request, sys, re

# Get detailed info on top AI stories
stories = [
    ("Cognition SWE-2", "https://cognition.com/blog/swe-2"),
    ("OpenAI Agents API", "https://developers.openai.com/api/docs/guides/agents-api/overview"),
    ("Anthropic Threat Intel", "https://www.anthropic.com/threat-intelligence-report-september-2026"),
    ("Compute-efficient pretraining", "https://magic.dev/blog/pretraining"),
    ("TokenSpeed LLM inference", "https://github.com/lightseekorg/tokenspeed"),
]

for name, url in stories:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"\n=== {name} ===")
        print(text[:600])
    except Exception as e:
        print(f"Error fetching {name}: {e}", file=sys.stderr)
