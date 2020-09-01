import sqlite3

conn = sqlite3.connect('side_project.db')
c=conn.cursor()
c.execute("SELECT * FROM members")
print(c.fetchall())
conn.commit()
conn.close()
