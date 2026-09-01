#!/usr/bin/env python3
"""Fetch details on specific AI stories"""
import re
import json, urllib.request, sys, urllib.parse

# Fetch top HN stories with more details
urls_to_check = [
    "https://news.ycombinator.com/item?id=49499867",  # Haiku R1/beta6
    "https://news.ycombinator.com/item?id=49498787",  # HuggingFace Hack
    "https://news.ycombinator.com/item?id=49499854",  # Omarchy
    "https://news.ycombinator.com/item?id=49499394",  # Encryption Backdoors
    "https://news.ycombinator.com/item?id=49502611",  # Continuous Diffusion LM
    "https://news.ycombinator.com/item?id=49497854",  # Automating Immersive Reading
    "https://news.ycombinator.com/item?id=49419381",  # Dad's AI coding
]

for url in urls_to_check:
    import subprocess
    result = subprocess.run(
        ["curl", "-s", "--max-time", "10", url],
        capture_output=True, text=True
    )
    title_m = re.findall(r'<title>(.*?)</title>', result.stdout)
    if title_m:
        print(f"{url} | {title_m[0]}")
