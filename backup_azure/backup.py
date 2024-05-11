import pyodbc
import sqlite3
import os
from datetime import datetime

# Azure SQL Database Connection Details
azure_server = 'bhmtest.database.windows.net'
azure_database = 'myTest'
azure_username = 'azureuser'
azure_password = 'T%nt0wn1'
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure you have the correct driver installed

# Tables to Backup
tables_to_backup = ['serve', 'tennis']

# Create backup directory if not exists
backup_folder = r'C:\code\python-flask-webapp\backup_db'
os.makedirs(backup_folder, exist_ok=True)

# SQLite Database File with current date
current_date = datetime.now().strftime('%Y-%m-%d')
sqlite_file = os.path.join(backup_folder, f'{current_date}.db')

# Connect to Azure SQL Database
azure_conn_str = f'DRIVER={driver};SERVER={azure_server};DATABASE={azure_database};UID={azure_username};PWD={azure_password}'
azure_conn = pyodbc.connect(azure_conn_str)
azure_cursor = azure_conn.cursor()

# Connect to SQLite Database
sqlite_conn = sqlite3.connect(sqlite_file)
sqlite_cursor = sqlite_conn.cursor()

# Backup Tables
for table in tables_to_backup:
    # Fetch data from Azure SQL Database
    azure_cursor.execute(f'SELECT * FROM {table}')
    rows = azure_cursor.fetchall()

    # Create table in SQLite and insert fetched data
    sqlite_cursor.execute(f'DROP TABLE IF EXISTS {table}')
    sqlite_cursor.execute(f'CREATE TABLE {table} ({", ".join([col[0] for col in azure_cursor.description])})')
    sqlite_cursor.executemany(f'INSERT INTO {table} VALUES ({", ".join(["?" for _ in range(len(azure_cursor.description))])})', rows)

# Commit changes and close connections
sqlite_conn.commit()
sqlite_conn.close()
azure_conn.close()

print(f"Tables {', '.join(tables_to_backup)} backed up successfully to SQLite database file: {sqlite_file}.")