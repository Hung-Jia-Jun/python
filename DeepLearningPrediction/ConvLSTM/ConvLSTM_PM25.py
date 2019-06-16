
# coding: utf-8
import math
import os
import pdb
import numpy
import csv
import matplotlib.pyplot as plt
from pandas import read_csv
from keras.layers import LSTM,Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers.convolutional import Conv3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization
import numpy as np
from matplotlib import pyplot as plt
from keras.models import model_from_json
import pickle
from sklearn.preprocessing import MinMaxScaler

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"



# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

#設定隨機生成亂數種子
numpy.random.seed(7)


#空氣監測資料list
POCDatas = []


# 載入訓練資料
dataframe = read_csv('FinalData/嘉義站(20100101-20190315)V1(Finish).csv', engine='python', skipfooter=3)
dataset = dataframe.values

dataset = dataset.flatten().reshape(-1, 1)

dataset = dataset.astype('float32')

#一天24hr *7天
#dataset = dataset[:168]

# 正規化(normalize) 資料，使資料值介於[0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))



#開始進行正規化
POCDatas = scaler.fit_transform(dataset)


# 2/3 資料為訓練資料， 1/3 資料為測試資料
train_size = int(len(POCDatas) * 0.67)
test_size = len(POCDatas) - train_size

train, test = POCDatas[0:train_size], POCDatas[train_size:len(POCDatas)]

look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0],trainX.shape[1],1,1,1))
trainY = numpy.reshape(trainY, (trainY.shape[0],1,1,1,1))
testX = numpy.reshape(testX,  (testX.shape[0],testX.shape[1],1,1,1))

# # Set ConvLSTM model
#=====================
print("CONVOLUTIONAL LSTM: SETTING MODELS ")

seq = Sequential()
seq.add(ConvLSTM2D(filters=30, kernel_size=(3, 3),
				   input_shape=(None, 1, 1, 1),
				   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=40, kernel_size=(4, 4),
				   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=50, kernel_size=(5, 5), 
				   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=50, kernel_size=(3, 3),
				   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(Conv3D(filters=1, kernel_size=(3, 3, 3),
			   activation='sigmoid',
			   padding='same', data_format='channels_last'))
seq.compile(loss='mean_squared_error', optimizer='adam',metrics=['acc'])

#====================

seq.summary()

seq.fit(trainX, trainY, epochs=200, batch_size=1, verbose=2)

# 預測
trainPredict = seq.predict(trainX)
testPredict = seq.predict(testX)


#重新將維度降回要輸出的 14,1
trainPredict = numpy.reshape(trainPredict, (trainPredict.shape[0],trainPredict.shape[1]))
testPredict = numpy.reshape(testPredict, (testPredict.shape[0],testPredict.shape[1]))


# 回復預測資料值為原始數據的規模
trainPredict = scaler.inverse_transform(trainPredict)

trainY = numpy.reshape(trainY, (trainY.shape[0]))


trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate 均方根誤差(root mean squared error)
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# 畫訓練資料趨勢圖
# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# 畫測試資料趨勢圖
# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

# 畫原始資料趨勢圖
plt.plot(scaler.inverse_transform(dataset)/50)
plt.plot(testPredictPlot-24)
plt.plot(trainPredictPlot-24)
plt.show()
