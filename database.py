import sqlite3 as sq

con=sq.connect("database.db")
c=con.cursor()

c.execute("create table feedback(id INTEGER  PRIMARY KEY AUTOINCREMENT,name TEXT,event_name TEXT,rating INTEGER,comments TEXT)")

con.commit()
con.close()
