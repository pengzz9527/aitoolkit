#!/usr/bin/env python3
"""Debug GitHub trending HTML parsing."""
import re

with open("/root/aitoolkit/scripts/.cache/github_trending.html") as f:
    html = f.read()

# Find a sample article
idx = html.find('<article class="Box-row">')
if idx >= 0:
    sample = html[idx:idx+2000]
    print("=== Sample Article HTML ===")
    print(sample[:2000])
    print("\n=== Looking for star patterns ===")
    # Find all star-related patterns
    for m in re.finditer(r'[\d,]+\s*stars', sample):
        print(f"  Found: '{m.group()}' at pos {m.start()}")
    for m in re.finditer(r'started', sample):
        print(f"  Found 'started' at pos {m.start()}")
        print(f"  Context: {sample[max(0,m.start()-50):m.start()+100]}")
