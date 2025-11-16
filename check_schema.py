import sqlite3

conn = sqlite3.connect('sql_runner.db')
cursor = conn.cursor()

print('recent_queries table schema:')
cursor.execute('PRAGMA table_info(recent_queries)')
for row in cursor.fetchall():
    print(row)

print('\nUsers table schema:')
cursor.execute('PRAGMA table_info(users)')
for row in cursor.fetchall():
    print(row)

conn.close()
