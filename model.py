import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from keras import layers
from keras.layers import Input, Dense, Activation
from keras.models import Model, Sequential
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning (from sklearn and seaborn)

def initModel(input_dim):
	X = Sequential()
	X.add(Dense(32, activation = "relu", input_shape = (input_dim, )))
	X.add(Dense(16, activation = "relu"))
	X.add(Dense(4, activation = "softmax"))
	return X

def train():
	x = pd.read_csv('grids.csv', sep = ';', header = None)
	y = pd.read_csv('moves.csv', sep = ';', header = None)
	y_one_hot = np.zeros((x.shape[0], 4))

	for i in range(x.shape[0]):
		y_one_hot[i][y.iloc[i]] = 1

	model = initModel(x.shape[1])
	model.compile(optimizer = "adam", loss	= "categorical_crossentropy", metrics = ['accuracy'])
	model.fit(x, y_one_hot, batch_size = 32, epochs = 100)
	return model



def predict(model, x):
	directions = ["left", "right", "up", "down"]
	df = pd.DataFrame(data = np.reshape(x, (1, 83)), index = [0], columns=[i for i in range(83)])
	predicts = model.predict(df).flatten()
	max_ind = np.argmax(predicts)
	return max_ind, directions[max_ind]