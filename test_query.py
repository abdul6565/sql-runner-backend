import sqlite3

conn = sqlite3.connect('sql_runner.db')
cursor = conn.cursor()

# Test the query
cursor.execute('SELECT * FROM customers')
results = cursor.fetchall()

print('Query executed successfully!')
print(f'Number of rows: {len(results)}')
print('First few rows:')
for i, row in enumerate(results[:3]):
    print(f'Row {i+1}: {row}')

conn.close()
