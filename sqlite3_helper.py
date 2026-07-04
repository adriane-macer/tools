import sqlite3


db_file = r'D:\Github\tools\target\sdu\Project.DB'
# Connect (creates the file if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

print(f'tables {tables}')

[print(x) for x in tables]
#
# # Retrieve data
# cursor.execute('SELECT * FROM users')
# print(cursor.fetchall())

conn.close()
