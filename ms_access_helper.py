import pyodbc

# Path to your Access file
msa_file = r'D:\Github\tools\target\sdu\Project.DB'

# Connection String
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb, *.db)};'
    r'DBQ=' + msa_file + ';'
)


# Establish connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Execute a SQL query
cursor.execute('SELECT * FROM TableName')

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()