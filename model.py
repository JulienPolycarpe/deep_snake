import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from keras import layers
from keras.layers import Input, Dense, Activation, Dropout
from keras.models import Model, Sequential
import warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning (from sklearn and seaborn)

def initModel(input_dim):
	X = Sequential()
	X.add(Dense(64, activation = "relu", input_shape = (input_dim, )))
	X.add(Dropout(0.20))
	X.add(Dense(64, activation = "relu"))
	X.add(Dropout(0.20))
	X.add(Dense(64, activation = "relu"))
	X.add(Dropout(0.20))
	X.add(Dense(16, activation = "relu"))
	#X.add(Dropout(0.20))
	X.add(Dense(1, activation = "sigmoid"))
	return X

def train():
	x = pd.read_csv('grids.csv', sep = ';', header = None)
	y = pd.read_csv('moves.csv', sep = ';', header = None)

	m = x.shape[0]
	parameters_nb = x.shape[1]

	train_ratio = 0.67
	test_ratio = 0.33
	#validation_ratio = 0.10

	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 - train_ratio)
	#x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=test_ratio/(test_ratio + validation_ratio))

	model = initModel(parameters_nb)
	model.compile(optimizer = "adam", loss	= "binary_crossentropy", metrics = ['accuracy'])

	history = model.fit(x_train, y_train, batch_size = 64, epochs = 3)
	#history = model.fit(pd.concat([x_train, x_test]), pd.concat([y_train, y_test]), validation_split = 0.1, batch_size = 64, epochs = 3)
	#history = model.fit(x, y, validation_split = 0.33, batch_size = 32, epochs = 10)
	"""
	plt.plot(history.history['accuracy'])
	plt.plot(history.history['val_accuracy'])
	plt.title('model accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc='upper left')
	plt.show()

	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc='upper left')
	plt.show()
	"""
	predict_y_test = []
	predictions = model.predict(x_test).flatten()
	print(m, x_train.shape[0] + x_test.shape[0], x_train.shape[0], x_test.shape[0], len(predictions))
	error_nb = 0
	for v in predictions:
		if v > 0.3:
			predict_y_test.append(1)
		else:
			predict_y_test.append(0)

	for v1, v2 in zip(predict_y_test, y_test):
		if v1 != v2:
			error_nb += 1

	print(error_nb)
	return 0



def predict(model, x):
	df = pd.DataFrame(data = np.reshape(x, (1, 6)), index = [0], columns=[i for i in range(6)])
	predicts = model.predict(df).flatten()
	return predicts

train()