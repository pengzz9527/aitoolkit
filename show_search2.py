import json
for p in ['/tmp/s4.json','/tmp/s5.json']:
    d=json.load(open(p))
    print(f"=== {p} total={d.get('total_count')} ===")
    for r in d.get('items',[]):
        lic=(r.get('license') or {}).get('spdx_id')
        print(f"  {r['stargazers_count']:>6} {r['full_name']:<45} | {lic} | {r.get('created_at','')[:10]} | {(r.get('description') or '')[:110]}")
