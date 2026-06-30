#!/usr/bin/env python3
"""Fetch GitHub trending repos."""
import json, urllib.request, sys
from html.parser import HTMLParser

class TitleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_link = False
        self.current_text = ""
        self.in_desc = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a' and attrs_dict.get('href','').startswith('/trend'):
            self.in_link = True
            self.current_text = ""
        if tag == 'p' and any('markdown-body' in c for c in attrs_dict.get('class', [])):
            self.in_desc = True
            
    def handle_data(self, data):
        if self.in_link:
            self.current_text += data
        if self.in_desc:
            self.results.append(data.strip())
            
    def handle_endtag(self, tag):
        if tag == 'a' and self.in_link:
            self.in_link = False
        if tag == 'p' and self.in_desc:
            self.in_desc = False

def fetch_github_trending():
    """Parse GitHub trending page manually."""
    req = urllib.request.Request(
        'https://github.com/trending?since=daily&spoken_language_code=',
        headers={'User-Agent': 'AI-Reporter/1.0', 'Accept': 'text/html'}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Parse manually with regex
        import re
        repos = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
        
        print("=== GITHUB TRENDING (Daily) ===")
        for i, repo_html in enumerate(repos[:20], 1):
            # Extract repo name
            h2_match = re.search(r'<h2.*?<a\s+href="/([^"]+)".*?>.*?</a>.*?</h2>', repo_html, re.DOTALL)
            # Extract title
            title_match = re.search(r'<svg[^>]*class="octicon"[^>]*>.*?</svg>\s*<a[^>]*>([^<]+)</a>', repo_html, re.DOTALL)
            # Extract stars
            stars_match = re.search(r'<span[^>]*class="d-inline-block[^"]*float-sm-[^"]*"[^>]*>([^<]+)</span>', repo_html)
            # Extract description
            desc_match = re.search(r'<p class="col-9[^\"]*".*?>([^<]+)</p>', repo_html, re.DOTALL)
            
            repo_path = h2_match.group(1) if h2_match else 'N/A'
            stars = stars_match.group(1).strip() if stars_match else 'N/A'
            desc = desc_match.group(1).strip() if desc_match else 'N/A'
            
            is_ai = any(kw in (repo_path + ' ' + desc).lower() for kw in 
                       ['ai', 'llm', 'gpt', 'openai', 'anthropic', 'model', 'ml', 
                        'neural', 'diffusion', 'agent', 'nlp', 'vision', 'llama',
                        'transformer', 'embedding', 'vector', 'chatbot', 'stable-diffusion',
                        'deep learning', 'robotics', 'computer-vision'])
            
            tag = " [AI/ML]" if is_ai else ""
            print(f"{i}. {repo_path} | ⭐ {stars}{tag}")
            if desc != 'N/A':
                print(f"   {desc[:120]}")
                
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}", file=sys.stderr)

fetch_github_trending()
