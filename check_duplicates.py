import duckdb
conn = duckdb.connect("/root/.hermes/backups/cron_history/cron_history.duckdb")
results = conn.execute("SELECT topic_title FROM published_topics LIMIT 100").fetchall()
print("=== 已发布选题 ===")
for r in results:
    print(f"  - {r[0]}")
