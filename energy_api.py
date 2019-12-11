import sqlite3
conn = sqlite3.connect('energy.db')

c = conn.cursor()

c.execute("SELECT * FROM dataRM")

print(c.fetchall())