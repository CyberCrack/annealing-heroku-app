import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT * FROM annealing;")
rows = cursor.fetchall()
for row in rows:
	print(row)
