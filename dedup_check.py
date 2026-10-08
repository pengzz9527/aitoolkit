import duckdb
conn = duckdb.connect("/root/.hermes/backups/cron_history/cron_history.duckdb")
try:
    rows = conn.execute("""
        SELECT topic_title, job_id, published_at, source
        FROM published_topics ORDER BY published_at DESC LIMIT 100
    """).fetchall()
except Exception as e:
    print("ERR:", e)
    tables = conn.execute("SHOW TABLES").fetchall()
    print("TABLES:", tables)
    rows = []
    for (t,) in tables:
        try:
            rs = conn.execute(f"SELECT * FROM {t} LIMIT 20").fetchall()
            print("---", t)
            for r in rs:
                print(r)
        except Exception as e2:
            print("ERR:", e2)
print("RECENT TOPICS (100):")
for r in rows:
    print(r[0])
