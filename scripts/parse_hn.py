#!/usr/bin/env python3
"""Parse HN Algolia data."""
import json
import sys

with open('/tmp/hn_algolia.json', 'r') as f:
    data = json.load(f)

hits = data.get('hits', [])
for h in hits[:25]:
    print(f"ID:{h.get('objectID','')} | Title:{h.get('title','')} | Score:{h.get('points',0)} | Comments:{h.get('num_comments',0)} | URL:{h.get('url','')} | Domain:{h.get('domain','')}")
