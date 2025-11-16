import sqlite3

conn = sqlite3.connect('sql_runner.db')
cursor = conn.cursor()
cursor.execute('SELECT username, password FROM users')
users = cursor.fetchall()
print('Users in database:')
for user in users:
    print(f'Username: {user[0]}, Password hash: {user[1]}')
conn.close()
