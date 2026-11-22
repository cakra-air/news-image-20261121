import sqlite3

uri = "file:C:/Users/User/.local/share/opencode/opencode.db?mode=ro"
c = sqlite3.connect(uri, uri=True)
print("tables:", [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")])
for name in ("session", "message", "part"):
    try:
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({name})")]
        print(name, "cols:", cols)
    except Exception as e:
        print(name, "ERR", e)
try:
    for r in c.execute("SELECT id, title, time_created FROM session ORDER BY time_created DESC LIMIT 10"):
        print("session:", r)
except Exception as e:
    print("session query ERR", e)
