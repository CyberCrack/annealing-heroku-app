import os
import psycopg2

import DeployableModel

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()


def checkDatabaseExists():
	sql = "SELECT to_regclass('annealing');"
	cursor.execute(sql)
	if cursor.fetchone()[0] == 'annealing':
		return True
	else:
		return False


def createDatabase():
	sql = '''CREATE TABLE annealing(
	   id SERIAL PRIMARY KEY,
	   family TEXT DEFAULT 'UNK',
	   product_type TEXT,
	   steel TEXT NOT NULL DEFAULT 'NA',
	   carbon REAL NOT NULL,
	   hardness REAL NOT NULL,
	   temper_rolling TEXT NOT NULL DEFAULT 'NA',
	   condition TEXT NOT NULL DEFAULT 'NA',
	   formability TEXT NOT NULL DEFAULT '0',
	   strength REAL NOT NULL,
	   non_ageing TEXT NOT NULL DEFAULT 'NA',
	   surface_finish TEXT NOT NULL DEFAULT 'NA',
	   surface_quality TEXT NOT NULL DEFAULT 'NA',
	   enamelability TEXT NOT NULL DEFAULT '0',
	   bc TEXT NOT NULL DEFAULT 'NA',
	   bf TEXT NOT NULL DEFAULT 'NA',
	   bt TEXT NOT NULL DEFAULT 'NA',
	   bw_me TEXT NOT NULL DEFAULT 'NA',
	   bl TEXT NOT NULL DEFAULT 'NA',
	   m TEXT NOT NULL DEFAULT 'NA',
	   chrom TEXT NOT NULL DEFAULT 'NA',
	   phos TEXT NOT NULL DEFAULT 'NA',
	   cbond TEXT NOT NULL DEFAULT 'NA',
	   marvi TEXT NOT NULL DEFAULT 'NA',
	   exptl TEXT NOT NULL DEFAULT 'NA',
	   ferro TEXT NOT NULL DEFAULT 'NA',
	   corr TEXT NOT NULL DEFAULT 'NA',
	   blue_bright_varn_clean TEXT NOT NULL DEFAULT 'NA',
	   lustre TEXT NOT NULL DEFAULT 'NA',
	   jurofm TEXT NOT NULL DEFAULT 'NA',
	   s TEXT NOT NULL DEFAULT 'NA',
	   p TEXT NOT NULL DEFAULT 'NA',
	   shape TEXT NOT NULL ,
	   thick REAL NOT NULL,
	   width REAL NOT NULL,
	   len REAL NOT NULL,
	   oil TEXT NOT NULL DEFAULT 'NA',
	   bore INTEGER NOT NULL,
	   packing INTEGER NOT NULL DEFAULT 0,
	   classes TEXT NOT NULL
	)'''
	cursor.execute(sql)
	conn.commit()


def insertData(data: dict):
	cursor.execute(
		"INSERT INTO annealing (family, product_type, steel, carbon, hardness, temper_rolling, condition, formability, strength, non_ageing, "
		"surface_finish, surface_quality, enamelability, bc, bf, bt, bw_me, bl, m, chrom, phos, cbond, marvi, exptl, ferro, corr, "
		"blue_bright_varn_clean, lustre, jurofm, s, p, shape, thick, width, len, oil, bore, packing, classes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
		"%s,%s,%s,%s,%s,"
		"%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
		tuple(data.values()))
	conn.commit()


def deleteData(id):
	cursor.execute("DELETE FROM annealing WHERE id=%s", (id,))
	conn.commit()
	return cursor.rowcount


def getRecentID():
	cursor.execute("SELECT last_value FROM annealing_id_seq;")
	return cursor.fetchone()[0]


def update(id: int, data: dict):
	col_index = {
		'family': 0, 'product_type': 1, 'steel': 2, 'carbon': 3, 'hardness': 4, 'temper_rolling': 5, 'condition': 6, 'formability': 7, 'strength': 8,
		'non_ageing': 9, 'surface_finish': 10, 'surface_quality': 11, 'enamelability': 12, 'bc': 13, 'bf': 14, 'bt': 15, 'bw_me': 16, 'bl': 17,
		'm': 18, 'chrom': 19, 'phos': 20, 'cbond': 21, 'marvi': 22, 'exptl': 23, 'ferro': 24, 'corr': 25, 'blue_bright_varn_clean': 26, 'lustre': 27,
		'jurofm': 28, 's': 29, 'p': 30, 'shape': 31, 'thick': 32, 'width': 33, 'len': 34, 'oil': 35, 'bore': 36, 'packing': 37, 'classes': 38
	}
	cursor.execute("SELECT family, product_type, steel, carbon, hardness, temper_rolling, condition, formability, strength, non_ageing, "
				   "surface_finish, surface_quality, enamelability, bc, bf, bt, bw_me, bl, m, chrom, phos, cbond, marvi, exptl, ferro, corr, "
				   "blue_bright_varn_clean, lustre, jurofm, s, p, shape, thick, width, len, oil, bore, packing, classes FROM annealing WHERE id = "
				   "%s",
				   (id,))
	returnValue = list(cursor.fetchone())
	for key in list(data.keys()):
		returnValue[col_index[key]] = data[key]
	returnValue.append(id)
	cursor.execute(
		"UPDATE annealing SET family = %s,product_type = %s,steel = %s,carbon = %s,hardness = %s,temper_rolling = %s,condition = %s,formability = "
		"%s,"
		"strength = %s,non_ageing = %s,surface_finish = %s,surface_quality = %s,enamelability = %s,bc = %s,bf = %s,bt = %s,bw_me = %s,bl = %s,"
		"m = %s,chrom = %s,"
		"phos = %s,cbond = %s,marvi = %s,exptl = %s,ferro = %s,corr = %s,blue_bright_varn_clean = %s,lustre = %s,jurofm = %s,s = %s,p = %s,"
		"shape = %s,thick = %s,"
		"width = %s,len = %s,oil = %s,bore = %s,packing = %s,classes = %s where id = %s", tuple(returnValue))

	conn.commit()
	return updateclass(id=id)


def updateclass(id):
	col_headings = ['family', 'product_type', 'steel', 'carbon', 'hardness', 'temper_rolling', 'condition', 'formability', 'strength', 'non_ageing',
					'surface_finish', 'surface_quality', 'enamelability', 'bc', 'bf', 'bt', 'bw_me', 'bl', 'm', 'chrom', 'phos', 'cbond', 'marvi',
					'exptl', 'ferro', 'corr', 'blue_bright_varn_clean', 'lustre', 'jurofm', 's', 'p', 'shape', 'thick', 'width', 'len', 'oil',
					'bore', 'packing', 'classes']
	cursor.execute("SELECT family, product_type, steel, carbon, hardness, temper_rolling, condition, formability, strength, non_ageing, "
				   "surface_finish, surface_quality, enamelability, bc, bf, bt, bw_me, bl, m, chrom, phos, cbond, marvi, exptl, ferro, corr, "
				   "blue_bright_varn_clean, lustre, jurofm, s, p, shape, thick, width, len, oil, bore, packing FROM annealing WHERE id = "
				   "%s",
				   (id,))
	returnValue = cursor.fetchone()
	data = {}
	for index in range(len(returnValue)):
		data[col_headings[index]] = returnValue[index]
	result = DeployableModel.getPredictions(data=data)
	cursor.execute("UPDATE annealing SET classes = %s WHERE id = %s", (result, id))
	conn.commit()
	return cursor.rowcount


exits = checkDatabaseExists()
if not exits:
	createDatabase()
