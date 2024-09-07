import sqlite3

sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()
print("DB Init")

query = 'select sqlite_version();'
cursor.execute(query)

result = cursor.fetchall()
print(f"SQLite Version is {result}")

cursor.execute('''DELETE FROM videos''')

cursor.close()
sqliteConnection.commit()
sqliteConnection.close()