import sqlite3
from datetime import timedelta 
from datetime import date 
# connect sql 
conn = sqlite3.connect("LibraryManagement.db")
print("Database connected")

# cursor use to execute sql commands
query = conn.cursor()
# query.execute('''
# CREATE TABLE if not exists admin(
# id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# username VARCHAR,
# password VARCHAR
# )
# ''')

# query.execute("INSERT INTO admin(username, password) values(?, ?)", ("admin", "pass1234"))

# query.execute('''UPDATE admin SET username = 'admin' WHERE password = 'pass1234';''')

# now = datetime.datetime.now()
date = date.today()
print(date)
Enddate = date + timedelta(days=15)

print(Enddate)
conn.commit()
conn.close()