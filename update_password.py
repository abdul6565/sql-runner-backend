import sqlite3
from passlib.hash import pbkdf2_sha256

conn = sqlite3.connect('sql_runner.db')
cursor = conn.cursor()

# Update dany's password
new_hash = pbkdf2_sha256.hash('dany123')
cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_hash, 'dany'))
conn.commit()

print('Updated dany password')
cursor.execute('SELECT username, password FROM users WHERE username = ?', ('dany',))
user = cursor.fetchone()
print(f'Updated user: {user}')

conn.close()
