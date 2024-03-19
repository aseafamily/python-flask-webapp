# now.date() - serves[0].date.date()
from datetime import datetime, timedelta

first = datetime.now()
fromDatabase = '2024-03-17 00:00:00'
fromDatabase_Obj = datetime.strptime(fromDatabase, '%Y-%m-%d %H:%M:%S')


days_since_last_serve = (first.date() - fromDatabase_Obj.date() - timedelta(hours=8)).days


print(first)
print(days_since_last_serve)