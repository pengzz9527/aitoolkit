import json
d=json.load(open('/root/.hermes/cron/output/innovation_projects_sent.json'))
for x in d:
    blob=json.dumps(x).lower()
    if 'esp32-iphone-agent' in blob or 'onehumanbeing' in blob:
        print('DATE:', x.get('date'), '| sent_at:', x.get('sent_at'), '| score:', x.get('score'), '| stars:', x.get('stars'))
