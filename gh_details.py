import json, glob

for path in sorted(glob.glob('/tmp/repo_*_new.json')) + sorted(glob.glob('/tmp/repo_onehumanbeing*.json')) + sorted(glob.glob('/tmp/repo_Leonxlnx*.json')) + sorted(glob.glob('/tmp/repo_HeyPuter*.json')) + sorted(glob.glob('/tmp/repo_Gathin23_cleanyourtv.json')) + sorted(glob.glob('/tmp/repo_KnifeLemon_Filee.json')):
    try:
        d = json.load(open(path))
    except Exception as e:
        print(path, 'ERR', e); continue
    print(f"=== {d.get('full_name')} === stars={d.get('stargazers_count')} forks={d.get('forks_count')} open_issues={d.get('open_issues_count')} license={(d.get('license') or {}).get('spdx_id')} created={d.get('created_at')} pushed={d.get('pushed_at')}")
    print('  ', (d.get('description') or '')[:200])
    print('  topics:', d.get('topics'))
