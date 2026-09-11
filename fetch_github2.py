#!/usr/bin/env python3
import json, urllib.request, sys, re

# Fetch GitHub AI-related repos with more stars
repos = [
    ("KiroCrew", "https://github.com/kirodotdev/KiroCrew"),
    ("sglang", "https://github.com/sgl-project/sglang"),
    ("executorch", "https://github.com/pytorch/executorch"),
    ("tokenspeed", "https://github.com/lightseekorg/tokenspeed"),
]

for name, url in repos:
    try:
        api_url = url.replace("github.com", "api.github.com/repos").replace("/$", "")
        # Get the repo info
        api_url = f"https://api.github.com/repos/{url.split('/')[-2]}/{url.split('/')[-1]}"
        req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        desc = data.get('description', '') or ''
        stars = data.get('stargazers_count', 0)
        lang = data.get('language', '')
        topics = data.get('topics', [])
        print(f"\n=== {name} ===")
        print(f"Stars: {stars} | Lang: {lang}")
        print(f"Description: {desc[:300]}")
        print(f"Topics: {topics}")
    except Exception as e:
        print(f"Error fetching {name}: {e}", file=sys.stderr)

# Also check GitHub trending page
print("\n\n=== GitHub Trending AI/ML Today ===")
try:
    req = urllib.request.Request("https://github.com/trending?since=daily&spoken_language_code=", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read().decode('utf-8', errors='ignore')
    # Extract repo names and descriptions
    pattern = r'<h2[^>]*>.*?<a[^>]*href="/([^"]+)"[^>]*>.*?</a>.*?</h2>'
    repos_found = re.findall(pattern, content, re.DOTALL)
    # Also get descriptions
    desc_pattern = r'<p[^>]*class="col-9[^"]*"[^>]*>(.*?)</p>'
    descs = re.findall(desc_pattern, content, re.DOTALL)
    stars_pattern = r'<a[^>]*class="Link[^"]*"[^>]*>\s*(\d[\d,\s]*)\s*Stars'
    stars_found = re.findall(stars_pattern, content)
    
    for i, repo in enumerate(repos_found[:15]):
        repo_name = repo.strip()
        star_str = stars_found[i] if i < len(stars_found) else '?'
        desc = descs[i].strip() if i < len(descs) else ''
        desc = re.sub(r'<[^>]+>', '', desc)[:120]
        print(f"{i+1}. {repo_name} | {star_str} stars | {desc}")
except Exception as e:
    print(f"GitHub trending error: {e}", file=sys.stderr)
