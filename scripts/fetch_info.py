#!/usr/bin/env python3
"""Fetch GitHub repo details for today's article."""
import json
import urllib.request
import base64

def fetch_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Reporter/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))

def fetch_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Reporter/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return base64.b64decode(data['content']).decode('utf-8')

# Fetch Kimi-K3
print("=== Kimi-K3 ===")
try:
    d = fetch_repo_info("MoonshotAI", "Kimi-K3")
    print(f"Stars: {d.get('stargazers_count')}")
    print(f"Forks: {d.get('forks_count')}")
    print(f"Language: {d.get('language')}")
    lic = d.get('license')
    print(f"License: {lic.get('name') if lic else 'N/A'}")
    print(f"Created: {d.get('created_at')}")
    print(f"Updated: {d.get('updated_at')}")
    print(f"Description: {d.get('description')}")
    print(f"Topics: {d.get('topics')}")
    print(f"Homepage: {d.get('homepage')}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== superpowers ===")
try:
    d = fetch_repo_info("obra", "superpowers")
    print(f"Stars: {d.get('stargazers_count')}")
    print(f"Forks: {d.get('forks_count')}")
    print(f"Language: {d.get('language')}")
    lic = d.get('license')
    print(f"License: {lic.get('name') if lic else 'N/A'}")
    print(f"Created: {d.get('created_at')}")
    print(f"Updated: {d.get('updated_at')}")
    print(f"Description: {d.get('description')}")
    print(f"Topics: {d.get('topics')}")
    readme = fetch_readme("obra", "superpowers")
    print(f"README:\n{readme[:2000]}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== qm ===")
try:
    d = fetch_repo_info("yc-software", "qm")
    print(f"Stars: {d.get('stargazers_count')}")
    print(f"Forks: {d.get('forks_count')}")
    print(f"Language: {d.get('language')}")
    lic = d.get('license')
    print(f"License: {lic.get('name') if lic else 'N/A'}")
    print(f"Created: {d.get('created_at')}")
    print(f"Updated: {d.get('updated_at')}")
    print(f"Description: {d.get('description')}")
    print(f"Topics: {d.get('topics')}")
    print(f"Homepage: {d.get('homepage')}")
except Exception as e:
    print(f"Error: {e}")
