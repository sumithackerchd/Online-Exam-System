import sqlite3

conn = sqlite3.connect("exam.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admin(id, username, password)
VALUES(1,'admin','admin123')
""")

conn.commit()
conn.close()

print("Exam Database Created Successfully")