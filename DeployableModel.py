import collections
import pickle
import time

import xgboost
from pandas import DataFrame


def getPredictions(data: dict):
	data = dict(data)
	col_to_drop = ['family', 'product_type', 'non_ageing', 'surface_finish', 'enamelability', 'bc', 'm', 'chrom', 'phos', 'cbond', 'marvi', 'exptl',
				   'ferro', 'corr', 'blue_bright_varn_clean', 'lustre', 'jurofm', 's', 'p']
	for col in col_to_drop:
		del data[col]
	labels = ['1', '2', '3', '5', 'U']
	allPredictions = []
	inputArray = list(data.values())
	col_headings = ['steel', 'carbon', 'hardness', 'temper_rolling', 'condition',
					'formability', 'strength', 'surface-quality', 'bf', 'bt', 'bw/me', 'bl',
					'shape', 'thick', 'width', 'len', 'oil', 'bore', 'packing']
	inputArray = DataFrame([inputArray], columns=col_headings)
	pickle_in = open("Best Models with Scaler/480274705219246898_AdaBoostModelV2GS.pickle", "rb")
	clf1 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/480274705219246898_AdaBoostModelV2GS_ColumnTransformer.pickle", "rb")
	scaler1 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler1.transform(inputArray)
	allPredictions.append(clf1.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/480274705219246898_LogisticRegressionModelV2GS.pickle", "rb")
	clf2 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/480274705219246898_LogisticRegressionModelV2GS_ColumnTransformer.pickle", "rb")
	scaler2 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler2.transform(inputArray)
	allPredictions.append(clf2.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/5454353605356565284_AdaBoostModelV2.pickle", "rb")
	clf3 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/5454353605356565284_AdaBoostModelV2_ColumnTransformer.pickle", "rb")
	scaler3 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler3.transform(inputArray)
	allPredictions.append(clf3.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/5454353605356565284_RandomForestModelV2.pickle", "rb")
	clf4 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/5454353605356565284_RandomForestModelV2_ColumnTransformer.pickle", "rb")
	scaler4 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler4.transform(inputArray)
	allPredictions.append(clf4.predict(scaledArray))

	clf5 = xgboost.XGBClassifier()
	clf5.load_model(fname="Best Models with Scaler/5454353605356565284_XGBClassifierModelV2.bin")
	pickle_in = open("Best Models with Scaler/5454353605356565284_XGBClassifierModelV2_ColumnTransformer.pickle", "rb")
	scaler5 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler5.transform(inputArray)
	allPredictions.append(clf5.predict(scaledArray))

	allPredictions = [int(prediction) for prediction in allPredictions]
	ctr = collections.Counter(allPredictions)
	return labels[ctr.most_common(1)[0][0]]


if __name__ == "__main__":
	startTime = time.time()
	data = {
		'family': 'GB', 'product_type': 'c', 'steel': 'R', 'carbon': 0, 'hardness': 0, 'temper_rolling': 'T', 'condition': 'A',
		'formability': '2', 'strength': 0, 'non_ageing': 'N', 'surface_finish': 'P', 'surface_quality': 'F', 'enamelability': '2', 'bc': 'NA',
		'bf': 'Y', 'bt': 'Y', 'bw_me': 'M', 'bl': 'Y', 'm': 'Y', 'chrom': 'C', 'phos': 'P', 'cbond': 'Y', 'marvi': 'Y', 'exptl': 'NA', 'ferro': 'Y',
		'corr': 'NA', 'blue_bright_varn_clean': 'C', 'lustre': 'Y', 'jurofm': 'Y', 's': 'Y', 'p': 'Y', 'shape': 'SHEET', 'thick': 0,
		'width': 400000, 'len': 50000, 'oil': 'Y', 'bore': 1000, 'packing': 0
	}
	print(getPredictions(data))
	print(time.time() - startTime)
