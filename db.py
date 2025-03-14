import sqlite3

conn = sqlite3.connect("library.db")  # SQLite Database Create
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        quantity INTEGER NOT NULL
    )
""")

conn.commit()
conn.close()

print("✅ SQLite Database and Books Table Created Successfully!")
