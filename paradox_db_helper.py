import pyodbc
import sqlite3
import pandas as pd

paradox_conn = pyodbc.connect(
    "DSN=EST3_SDU_DSN;"
)
msa_file = r'D:\Github\tools\target\sdu\Project.DB'
sqlite_conn = sqlite3.connect("est3_sdu.sqlite")

tables = pd.read_sql(
    "SELECT * FROM project",
    paradox_conn
)

tables.to_sql("project", sqlite_conn, if_exists="replace", index=False)

sqlite_conn.close()
paradox_conn.close()
