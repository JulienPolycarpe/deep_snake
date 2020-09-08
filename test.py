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

def model(input_dim):
	X = Sequential()
	X.add(Dense(32, activation = "relu", input_shape = (input_dim, )))
	X.add(Dense(16, activation = "relu"))
	X.add(Dense(4, activation = "softmax"))
	return X

move = [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0, -1,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  1,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0]]

final_move = np.reshape(move, (1, 81))

x = pd.read_csv('grids.csv', sep = ';', header = None)
y = pd.read_csv('moves.csv', sep = ';', header = None)
y_one_hot = np.zeros((x.shape[0], 4))

for i in range(x.shape[0]):
	y_one_hot[i][y.iloc[i]] = 1

print(x.shape, y_one_hot.shape)
print(x)
print(y)
print(final_move)

final_move_df = pd.DataFrame(data = final_move, index = [0], columns=[i for i in range(81)])
print(final_move_df)

model = model(x.shape[1])
model.compile(optimizer = "adam", loss	= "categorical_crossentropy", metrics = ['accuracy'])
model.fit(x, y_one_hot, batch_size = 16, epochs = 100)
test = model.predict(final_move).flatten()
#left right up down
#
print(test, np.argmax(test))
"""
for x in move:
	print(x)
"""