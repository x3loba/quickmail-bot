# language: Python, file: db.py
import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS combos (
  combo TEXT PRIMARY KEY, status TEXT, attempts INT DEFAULT 0, ts INTEGER
);
CREATE TABLE IF NOT EXISTS hits (
  email TEXT, password TEXT, keyword TEXT, ts INTEGER
);
"""

async def init(path="quickmail.db"):
    db = await aiosqlite.connect(path)
    await db.executescript(SCHEMA)
    await db.commit()
    return db

async def mark(db, combo, status):
    await db.execute(
      "INSERT INTO combos(combo,status,attempts,ts) VALUES(?,?,1,strftime('%s','now')) "
      "ON CONFLICT(combo) DO UPDATE SET status=excluded.status, attempts=attempts+1, ts=excluded.ts",
      (combo, status))
    await db.commit()
