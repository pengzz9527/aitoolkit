#!/usr/bin/env python3
import json, urllib.request

repos = [
    "sapientinc/PRAXIST",
    "anthropics/commerce-agents",
    "ApodexAI/FrontierAgent",
    "Tencent/WeMM-Embedding",
    "2akouwu/reverify",
    "brayonpi/hexstellar",
    "lnkiai/m3e-canvas",
]

for repo in repos:
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        name = data.get("full_name", "")
        stars = data.get("stargazers_count", 0)
        desc = data.get("description", "") or ""
        lang = data.get("language", "")
        topics = data.get("topics", [])
        url_r = data.get("html_url", "")
        updated = data.get("updated_at", "")[:10]
        print(f"REPO|{name}|{stars}|{lang}|{updated}|{desc[:150]}|{url_r}|{','.join(topics)}")
    except Exception as e:
        print(f"ERROR|{repo}|{e}")
