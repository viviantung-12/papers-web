print("Hello, world!")

import sqlite3

conn = sqlite3.connect("papers.db")
c = conn.cursor()
c.execute("SELECT * FROM papers")
rows = c.fetchall()
print(rows)
conn.close()
