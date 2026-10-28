import json
for p in ['/tmp/repo_fmt.json','/tmp/repo_urm.json','/tmp/repo_ccbaga.json','/tmp/repo_cmath.json']:
    d=json.load(open(p))
    print(f"=== {d.get('full_name')} === stars={d.get('stargazers_count')} forks={d.get('forks_count')} open_issues={d.get('open_issues_count')} license={(d.get('license') or {}).get('spdx_id')} created={d.get('created_at')} pushed={d.get('pushed_at')}")
    print('  desc:', (d.get('description') or '')[:200])
    print('  topics:', d.get('topics'))
    print('  homepage:', d.get('homepage'))
