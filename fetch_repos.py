#!/usr/bin/env python3
import json, urllib.request, sys

repos = [
    "browser-use/browser-use",
    "ATH-MaaS/Pixelle-Video",
    "docling-project/docling",
    "jundot/omlx",
    "mukul975/Anthropic-Cybersecurity-Skills",
    "Tencent/AI-Infra-Guard",
    "opensearch-project/opensearch-py",
    "microsoft/agent-framework",
]

for r in repos:
    try:
        url = f"https://api.github.com/repos/{r}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.load(resp)
        print(f"{r} | ⭐{d['stargazers_count']} | {d.get('description','')[:100]}")
    except Exception as e:
        print(f"{r} | ERROR: {e}")
