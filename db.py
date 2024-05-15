from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db_uri = 'mssql+pyodbc://azureuser:T%nt0wn1@bhmtest.database.windows.net/myTest?driver=ODBC+Driver+17+for+SQL+Server&connect_timeout=30'