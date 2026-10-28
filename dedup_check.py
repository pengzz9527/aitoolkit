import json
d=json.load(open('/root/.hermes/cron/output/innovation_projects_sent.json'))
print('total sent:', len(d))
keys = ['onehumanbeing','esp32-iphone-agent','earshot','HeyPuter','cleanyourtv','Filee','aerial-tv','nxnative','d2r-mobile','free-my-tv','anatomy','DeepInfer','math']
names = [ (x.get('project_name','')+' '+x.get('repo','')) for x in d]
for k in keys:
    hits = [n for n in names if k in n.lower()]
    print(f"{k}: {len(hits)} sent hits")
    for h in hits[:3]: print('   ', h)
# pool
import io
pool=[]
try:
    for line in open('/root/.hermes/cron/output/innovation_pool.jsonl'):
        line=line.strip()
        if line:
            try: pool.append(json.loads(line))
            except: pass
except FileNotFoundError: pass
print('pool entries:', len(pool))
for p in pool:
    blob = json.dumps(p).lower()
    for k in keys:
        if k.lower() in blob:
            print(f"POOL {k}: {p.get('project')} {p.get('repo')} score={p.get('score')} ts={p.get('ts')}")
