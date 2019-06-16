import numpy as np, scipy.ndimage, matplotlib.pyplot as plt
from scipy import stats
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, ConvLSTM2D, MaxPooling2D, UpSampling2D
from sklearn.metrics import accuracy_score, confusion_matrix, cohen_kappa_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
np.random.seed(123)

raw = np.arange(96).reshape(8,3,4)
data1 = scipy.ndimage.zoom(raw, zoom=(1,100,100), order=1, mode='nearest') #low res
print (data1.shape)
#(8, 300, 400)

data2 = scipy.ndimage.zoom(raw, zoom=(1,100,100), order=3, mode='nearest') #high res
print (data2.shape)
#(8, 300, 400)

X_train = data1.reshape(1, data1.shape[0], data1.shape[1], data1.shape[2], 1)
Y_train = data2.reshape(1, data2.shape[0], data2.shape[1], data2.shape[2], 1)

model = Sequential()
input_shape = (data1.shape[0], data1.shape[1], data1.shape[2], 1)
model.add(ConvLSTM2D(16, kernel_size=(3, 3), activation='sigmoid', padding='same',input_shape=input_shape,return_sequences=True))
model.add(ConvLSTM2D(1, kernel_size=(3, 3), activation='sigmoid', padding='same',return_sequences=True))
model.compile(loss='mse', optimizer='adam')

model.fit(X_train, Y_train, 
      batch_size=1, epochs=10, verbose=1)

y_predict = model.predict(X_train)
y_predict = y_predict.reshape(data1.shape[0], data1.shape[1], data1.shape[2])
slope, intercept, r_value, p_value, std_err = stats.linregress(data2[0,:,:].reshape(-1), y_predict[0,:,:].reshape(-1))
print (r_value**2)