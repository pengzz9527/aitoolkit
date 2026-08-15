#!/usr/bin/env python3
import json, urllib.request, sys

repos = [
    "KKKKhazix/human-writing",
    "pathwaycom/arc-task-gen",
    "guillaumemeyer/watermarks-remover",
    "LaoFeng-mouse/flyingmouse-format",
    "thebuggeddev/anatomy",
    "ShawnPana/phone-harness",
    "oil-oil/oil-motion",
    "Binaryify/open-kimi-ppt-skill",
    "eternityspring/shuohao-skills",
    "jd-opensource/JoyAI-Video-Edit",
    "antirez/h3.c",
]

for repo in repos:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read())
            print(f"\n=== {repo} ===")
            print(f"Desc: {d.get('description', '')}")
            print(f"Stars: {d.get('stargazers_count')}")
            print(f"Lang: {d.get('language')}")
            print(f"URL: {d.get('html_url')}")
            print(f"Created: {d.get('created_at')}")
            print(f"Topics: {d.get('topics', [])}")
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
