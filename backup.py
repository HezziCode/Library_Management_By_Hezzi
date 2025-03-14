import sqlite3

# Backup banane ke liye database open karo
conn = sqlite3.connect("library.db")
backup_conn = sqlite3.connect("backup_library.db")

# Backup execute karo
with backup_conn:
    conn.backup(backup_conn)

conn.close()
backup_conn.close()

print("✅ Database Backup Successfully Created as 'backup_library.db'")
