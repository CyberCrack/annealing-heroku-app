import os
import sqlite3

import DeployableModel

databaseExits = True
if not os.path.exists("annealingDB.db"):
	databaseExits = False
conn = sqlite3.connect('annealingDB.db', check_same_thread=False)
cursor = conn.cursor()


def createDatabase():
	sql = '''CREATE TABLE annealing(
	   id INTEGER PRIMARY KEY AUTOINCREMENT,
	   family TEXT DEFAULT "UNK",
	   product_type TEXT,
	   steel TEXT NOT NULL DEFAULT "NA",
	   carbon REAL NOT NULL,
	   hardness REAL NOT NULL,
	   temper_rolling TEXT NOT NULL DEFAULT "NA",
	   condition TEXT NOT NULL DEFAULT "NA",
	   formability TEXT NOT NULL DEFAULT "0",
	   strength REAL NOT NULL,
	   non_ageing TEXT NOT NULL DEFAULT "NA",
	   surface_finish TEXT NOT NULL DEFAULT "NA",
	   surface_quality TEXT NOT NULL DEFAULT "NA",
	   enamelability TEXT NOT NULL DEFAULT "0",
	   bc TEXT NOT NULL DEFAULT "NA",
	   bf TEXT NOT NULL DEFAULT "NA",
	   bt TEXT NOT NULL DEFAULT "NA",
	   bw_me TEXT NOT NULL DEFAULT "NA",
	   bl TEXT NOT NULL DEFAULT "NA",
	   m TEXT NOT NULL DEFAULT "NA",
	   chrom TEXT NOT NULL DEFAULT "NA",
	   phos TEXT NOT NULL DEFAULT "NA",
	   cbond TEXT NOT NULL DEFAULT "NA",
	   marvi TEXT NOT NULL DEFAULT "NA",
	   exptl TEXT NOT NULL DEFAULT "NA",
	   ferro TEXT NOT NULL DEFAULT "NA",
	   corr TEXT NOT NULL DEFAULT "NA",
	   blue_bright_varn_clean TEXT NOT NULL DEFAULT "NA",
	   lustre TEXT NOT NULL DEFAULT "NA",
	   jurofm TEXT NOT NULL DEFAULT "NA",
	   s TEXT NOT NULL DEFAULT "NA",
	   p TEXT NOT NULL DEFAULT "NA",
	   shape TEXT NOT NULL ,
	   thick REAL NOT NULL,
	   width REAL NOT NULL,
	   len REAL NOT NULL,
	   oil TEXT NOT NULL DEFAULT "NA",
	   bore INTEGER NOT NULL,
	   packing INTEGER NOT NULL DEFAULT 0,
	   classes TEXT NOT NULL
	)'''
	cursor.execute(sql)


def insertData(data: dict):
	cursor.execute(
		"INSERT INTO annealing (family, product_type, steel, carbon, hardness, temper_rolling, condition, formability, strength, non_ageing, "
		"surface_finish, surface_quality, enamelability, bc, bf, bt, bw_me, bl, m, chrom, phos, cbond, marvi, exptl, ferro, corr, "
		"blue_bright_varn_clean, lustre, jurofm, s, p, shape, thick, width, len, oil, bore, packing, classes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
		"?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
		tuple(data.values()))
	conn.commit()


def deleteData(id):
	cursor.execute("DELETE FROM annealing WHERE id=?", (id,))
	conn.commit()
	return cursor.rowcount


def getRecentID():
	cursor.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name='annealing';")
	return cursor.fetchall()[0][0]


if not databaseExits:
	createDatabase()


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
				   "?",
				   (id,))
	returnValue = list(cursor.fetchone())
	for key in list(data.keys()):
		returnValue[col_index[key]] = data[key]
	returnValue.append(id)
	cursor.execute(
		"UPDATE annealing SET family = ?,product_type = ?,steel = ?,carbon = ?,hardness = ?,temper_rolling = ?,condition = ?,formability = ?,"
		"strength = ?,non_ageing = ?,surface_finish = ?,surface_quality = ?,enamelability = ?,bc = ?,bf = ?,bt = ?,bw_me = ?,bl = ?,m = ?,chrom = ?,"
		"phos = ?,cbond = ?,marvi = ?,exptl = ?,ferro = ?,corr = ?,blue_bright_varn_clean = ?,lustre = ?,jurofm = ?,s = ?,p = ?,shape = ?,thick = ?,"
		"width = ?,len = ?,oil = ?,bore = ?,packing = ?,classes = ? where id = ?", tuple(returnValue))

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
				   "?",
				   (id,))
	returnValue = cursor.fetchone()
	data = {}
	for index in range(len(returnValue)):
		data[col_headings[index]] = returnValue[index]
	result = DeployableModel.getPredictions(data=data)
	cursor.execute("UPDATE annealing SET classes = ? WHERE id = ?", (result, id))
	conn.commit()
	return cursor.rowcount


