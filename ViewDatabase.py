import sqlite3
conn = sqlite3.connect('annealingDB.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT * FROM annealing;")
rows = cursor.fetchall()
col_headings = ['family', 'product_type', 'steel', 'carbon', 'hardness', 'temper_rolling', 'condition', 'formability', 'strength', 'non_ageing',
				'surface_finish', 'surface_quality', 'enamelability', 'bc', 'bf', 'bt', 'bw_me', 'bl', 'm', 'chrom', 'phos', 'cbond', 'marvi',
				'exptl', 'ferro', 'corr', 'blue_bright_varn_clean', 'lustre', 'jurofm', 's', 'p', 'shape', 'thick', 'width', 'len', 'oil', 'bore',
				'packing', 'classes']
print("ID\t" +"\t".join(col_headings) )
for row in rows:
	print(row)