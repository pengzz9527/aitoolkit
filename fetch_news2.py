#!/usr/bin/env python3
"""Fetch more AI news from HN and GitHub for daily report."""
import urllib.request, json, urllib.parse

def fetch_hn(query):
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=front_page&hitsPerPage=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return data.get("hits", [])

print("=== AI AGENT ===")
for h in fetch_hn("AI agent")[:5]:
    pts = h.get("points", 0)
    url = h.get("url") or h.get("hn_url", "")
    print(f"[{pts}] {h['title']} | {url}")

print("\n=== LLM MODEL ===")
for h in fetch_hn("LLM model open source")[:5]:
    pts = h.get("points", 0)
    url = h.get("url") or h.get("hn_url", "")
    print(f"[{pts}] {h['title']} | {url}")

print("\n=== NEMOTRON NVIDIA ===")
for h in fetch_hn("Nemotron NVIDIA")[:5]:
    pts = h.get("points", 0)
    url = h.get("url") or h.get("hn_url", "")
    print(f"[{pts}] {h['title']} | {url}")

print("\n=== MOJO ===")
for h in fetch_hn("Mojo language")[:5]:
    pts = h.get("points", 0)
    url = h.get("url") or h.get("hn_url", "")
    print(f"[{pts}] {h['title']} | {url}")

print("\n=== GITHUB REPOS ===")
url = "https://api.github.com/search/repositories?q=stars:>500&created:>2026-08-11&sort=stars&order=desc&per_page=10"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())
for repo in data.get("items", [])[:8]:
    desc = (repo.get("description") or "")[:150]
    print(f"⭐{repo['stargazers_count']} {repo['full_name']} [{repo.get('language','')}] | {desc} | {repo['html_url']}")

print("\n=== GROK XAI ===")
for h in fetch_hn("Grok X AI bot")[:5]:
    pts = h.get("points", 0)
    url = h.get("url") or h.get("hn_url", "")
    print(f"[{pts}] {h['title']} | {url}")
