from flask import Flask, jsonify, request, render_template

# import SQLite3Database as Database
import PostgresqlDatabase as Database
from DeployableModel import getPredictions

app = Flask(__name__)
col_headings = ['family', 'product_type', 'steel', 'carbon', 'hardness', 'temper_rolling', 'condition', 'formability', 'strength', 'non_ageing',
				'surface_finish', 'surface_quality', 'enamelability', 'bc', 'bf', 'bt', 'bw_me', 'bl', 'm', 'chrom', 'phos', 'cbond', 'marvi',
				'exptl', 'ferro', 'corr', 'blue_bright_varn_clean', 'lustre', 'jurofm', 's', 'p', 'shape', 'thick', 'width', 'len', 'oil', 'bore',
				'packing', 'classes']
validValues = {
	'family': ["UNK", "ZS", "TN", "GB", "GK", "GS", "ZA", "ZF", "ZH", "ZM"], 'product_type': ["C", "H", "G"],
	'steel': ["NA", "A", "R", "K", "S", "M", "V", "W"], 'temper_rolling': ["NA", "T"], 'condition': ["NA", "A", "S"],
	'formability': ["0", "1", "2", "3", "4", "5"], 'non_ageing': ["NA", "N"], 'surface_finish': ["NA", "P", "M"],
	'surface_quality': ["NA", "D", "E", "F", "G"], 'enamelability': ["NA", "1", "2", "3", "4", "5"], 'bc': ["NA", "Y"], 'bf': ["NA", "Y"],
	'bt': ["NA", "Y"], 'bw_me': ["NA", "B", "M"], 'bl': ["NA", "Y"], 'm': ["NA", "Y"], 'chrom': ["NA", "C"],
	'phos': ["NA", "P"], 'cbond': ["NA", "Y"], 'marvi': ["NA", "Y"], 'exptl': ["NA", "Y"], 'ferro': ["NA", "Y"], 'corr': ["NA", "Y"],
	'blue_bright_varn_clean': ["NA", "B", "C", "V"], 'lustre': ["NA", "Y"], 'jurofm': ["NA", "Y"], 's': ["NA", "Y"], 'p': ["NA", "Y"],
	'shape': ["COIL", "SHEET"], 'oil': ["NA", "Y", "N"], 'packing': [0, 2, 3]
}
floatCols = ['thick', 'width']
intCols = ['carbon', 'hardness', 'strength', 'len', 'bore', 'packing']


@app.route('/', methods=['GET', 'POST'])
def home():
	data = {}
	if request.method == "POST":
		for feature in col_headings[:-1]:
			if feature in floatCols:
				try:
					data[feature] = abs(float(request.form[feature]))
				except ValueError:
					return jsonify("ERROR")
			elif feature in intCols:
				try:
					data[feature] = abs(int(float(request.form[feature])))
				except ValueError:
					return jsonify("ERROR")
			else:
				data[feature] = request.form[feature]
		result = getPredictions(data)
		data['classes'] = result
		Database.insertData(data=data)
		try:
			return render_template("result.html", result=result)
		except Exception:
			return jsonify("ERROR")
	return render_template("home.html")


@app.route('/api', methods=['POST'])
def postAPI():
	data = {}
	recv_data = request.get_json()
	for feature in col_headings[:-1]:
		if feature in floatCols:
			try:
				data[feature] = abs(float(recv_data[feature]))
			except ValueError:
				return jsonify("ERROR")
		elif feature in intCols:
			try:
				data[feature] = abs(int(float(recv_data[feature])))
			except ValueError:
				return jsonify("ERROR")
		else:
			if recv_data[feature] in validValues[feature]:
				data[feature] = recv_data[feature]
			else:
				return jsonify("ERROR: Check " + feature)
	result = getPredictions(data=data)
	data['classes'] = result
	Database.insertData(data=data)
	id = Database.getRecentID()
	return jsonify(id=id, Prediction=result)


@app.route('/api', methods=['PUT'])
def putAPI():
	data = {}
	recv_data: dict = request.get_json()
	try:
		id = recv_data['id']
	except KeyError:
		return jsonify("ERROR: id required")
	if type(id) == str or type(id) == float:
		return jsonify("ERROR: id should be a int value")

	for feature in col_headings[:-1]:
		if feature in floatCols:
			try:
				data[feature] = abs(float(recv_data[feature]))
			except ValueError:
				return jsonify("ERROR")
			except KeyError:
				pass
		elif feature in intCols:
			try:
				data[feature] = abs(int(float(recv_data[feature])))
			except ValueError:
				return jsonify("ERROR")
			except KeyError:
				pass
		else:
			try:
				if recv_data[feature] in validValues[feature]:
					data[feature] = recv_data[feature]
				else:
					return jsonify("ERROR: Check " + feature)
			except KeyError:
				pass

	updatecount = Database.update(id=id, data=data)
	if updatecount == 1:
		return jsonify(id=id, Successful=True)
	else:
		return jsonify(id=id, Successful=False)


@app.route('/api', methods=['DELETE'])
def deleteAPI():
	recv_data: dict = request.get_json()
	try:
		id = recv_data['id']
	except KeyError:
		return jsonify("ERROR: id required")
	if type(id) == str or type(id) == float:
		return jsonify("ERROR: id should be a int value")

	updateCount = Database.deleteData(id=id)
	if updateCount != 0 and updateCount is not None:
		return jsonify(id=id, Successful=True)
	else:
		return jsonify(id=id, Successful=False)


# driver function
if __name__ == '__main__':
	app.run(debug=False)
