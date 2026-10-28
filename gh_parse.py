import json, sys

def show(path, n):
    d = json.load(open(path))
    print(f"--- {path} total_count={d.get('total_count')} ---")
    for r in d.get("items", [])[:n]:
        lic = r.get("license", {}).get("spdx_id") if r.get("license") else "none"
        print(f"{r['stargazers_count']:>7} {r['full_name']:<45} | {lic:<15} | {r.get('created_at','')[:10]} | {(r.get('description') or '')[:120]}")

show("/tmp/gh_recent.json", 15)
show("/tmp/gh_new.json", 20)
