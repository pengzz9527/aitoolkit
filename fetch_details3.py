#!/usr/bin/env python3
import urllib.request, re, sys

# Get MCP details
url = 'https://blog.modelcontextprotocol.io/posts/mcp-roadmap/'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    # Get the first few paragraphs of content
    content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"MCP Roadmap content (first 500 chars): {text[:500]}")
    print()
except Exception as e:
    print(f"Error: {e}")

# Get ElevenLabs details
url2 = 'https://quantumi.sh/public/labs.html'
try:
    req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"ElevenLabs Labs content (first 500 chars): {text[:500]}")
    print()
except Exception as e:
    print(f"Error: {e}")

# Get Munder Difflin details
url3 = 'https://munderdiffl.in/'
try:
    req = urllib.request.Request(url3, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    content = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"Munder Difflin content (first 500 chars): {text[:500]}")
    print()
except Exception as e:
    print(f"Error: {e}")
