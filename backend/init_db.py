import sqlite3

conn = sqlite3.connect("gomoku.db")
cur = conn.cursor()

# 玩家
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_uuid TEXT,
    status TEXT,   -- "playing", "finished"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# 每一步棋
cur.execute("""
CREATE TABLE IF NOT EXISTS moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    row INTEGER,
    col INTEGER,
    player INTEGER,
    move_num INTEGER
)
""")

conn.commit()
conn.close()

print("Database initialized!")