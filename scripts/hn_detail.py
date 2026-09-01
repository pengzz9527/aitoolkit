#!/usr/bin/env python3
"""Get more HN detail on key stories"""
import subprocess, re

stories = [
    "49499867",  # Haiku R1/beta6
    "49499854",  # Omarchy
    "49499394",  # Encryption Backdoors
    "49498787",  # HuggingFace Hack
    "49497854",  # Automating Immersive Reading
]

for sid in stories:
    url = f"https://news.ycombinator.com/item?id={sid}"
    result = subprocess.run(
        ["curl", "-s", "--max-time", "10", url, "-H", "User-Agent: Mozilla/5.0"],
        capture_output=True, text=True
    )
    title_m = re.findall(r'<span class="titleline"[^>]*>.*?<a[^>]*>(.*?)</a>', result.stdout, re.DOTALL)
    points_m = re.findall(r'<span[^>]*class="score"[^>]*>(.*?)</span>', result.stdout)
    if title_m:
        title = re.sub(r'<[^>]+>', '', title_m[0]).strip()
        points = points_m[0] if points_m else ""
        print(f"[{points}] {title} | {url}")
        
        # Get first few comments
        comments = re.findall(r'<tr class="athing"[^>]*>.*?<span class="titleline">.*?<a[^>]*>(.*?)</a>.*?</td>.*?<span class="rank">(\d+)</span>.*?<span class="score">.*?(\d+) point</span>', result.stdout, re.DOTALL)
        for c_title, rank, pts in comments[:3]:
            ct = re.sub(r'<[^>]+>', '', c_title).strip()
            print(f"  #{rank} [{pts}pts] {ct[:100]}")
    else:
        print(f"--- No title for {sid}")
        # Try alternative pattern
        alt = re.findall(r'<span[^>]*class="[^\"]*titleline[^\"]*"[^>]*>(.*?)</span>', result.stdout, re.DOTALL)
        if alt:
            print(f"  Alt title: {re.sub(r'<[^>]+>', '', alt[0]).strip()}")
