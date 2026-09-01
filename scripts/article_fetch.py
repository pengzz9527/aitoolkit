#!/usr/bin/env python3
"""Fetch article content for key stories"""
import subprocess, re, sys

stories = [
    ("https://thezvi.wordpress.com/2026/08/29/metr-and-redwood-offer-holy-postmortem-of-the-huggingface-hack/", "HuggingFace Hack"),
    ("https://sander.ai/2026/08/24/continuous-dlms.html", "Continuous Diffusion LM"),
]

for url, name in stories:
    print(f"\n=== {name}: {url} ===")
    result = subprocess.run(
        ["curl", "-s", "--max-time", "15", url, "-H", "User-Agent: Mozilla/5.0"],
        capture_output=True, text=True
    )
    # Extract main text
    text = re.sub(r'<script[^>]*>.*?</script>', '', result.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    print(text[:500])
    print("...")
