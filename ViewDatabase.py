import sqlite3
conn = sqlite3.connect('annealingDB.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT * FROM annealing;")
rows = cursor.fetchall()
for row in rows:
	print(row)