#!/usr/bin/env python3
import re

for fname, label in [('/tmp/v1.html', 'Greg Brockman'), ('/tmp/v2.html', 'Hugging Face Hack'), ('/tmp/v3.html', 'Watermarks'), ('/tmp/v4.html', 'Disbanded Team'), ('/tmp/v5.html', 'Hit Brakes')]:
    try:
        with open(fname) as f:
            html = f.read()
        content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        # Find the article body
        # Look for common article body patterns
        body = text[500:2000] if len(text) > 500 else text
        print(f"=== {label} (body excerpt) ===")
        print(body[:400])
        print()
    except Exception as e:
        print(f"Error {label}: {e}")
