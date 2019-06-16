
# coding: utf-8

# In[ ]:


from sklearn.preprocessing import StandardScaler  
a = np.array([1,2,3,4,5,6,7,8,9,10])
scaler = MinMaxScaler(feature_range=(0, 1))

a = numpy.reshape (a,(-1,1))
a = scaler.fit_transform(a)
print (a)

a = scaler.inverse_transform(a)
print (a)


# In[19]:


# LSTM for international airline passengers problem with regression framing
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import pdb

import numpy as np

import keras.backend.tensorflow_backend as KTF
import tensorflow as tf
config = tf.ConfigProto()  
config.gpu_options.allow_growth=True   
session = tf.Session(config=config)
KTF.set_session(session)


# 產生 (X, Y) 資料集, Y 是下一期的乘客數
def create_dataset(dataset, look_back=10):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

# 載入訓練資料
dataframe = read_csv('C:\\Users\\Jason\\Anaconda3\\Scripts\\Bejin_Car_LSTM\\ConvLSTM\\pk10.csv', usecols=[2,3,4,5,6,7,8,9,10,11], engine='python', skipfooter=0)
#dataframe = read_csv('/Users/Jason/Scripts/ConvLSTM/Airplan.csv', usecols=[1], engine='python', skipfooter=3)

dataset = dataframe.values
dataset = dataset.astype('float32')

#使用前1000個資料，因為運算量巨大，會算太久
dataset = dataset[:100]

#扁平化所有資料，這樣資料就能以一維參數做預測學習他的排列組合模式
dataset = dataset.flatten()

#轉換Array維度，讓fit_transform可以運作
dataset = numpy.reshape (dataset,(-1,1))


# 正規化(normalize) 資料，使資料值介於[0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))

dataset = scaler.fit_transform(dataset)

# 2/3 資料為訓練資料， 1/3 資料為測試資料
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# 產生 (X, Y) 資料集, Y 是下一個數字(reshape into X=t and Y=t+1)
look_back = 1


trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
import pdb
pdb.set_trace()
print ("OK")


# In[20]:



# 建立及訓練 LSTM 模型
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)


# In[23]:


import pdb
import numpy as np
# 預測
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)



#trainPredict = scaler.inverse_transform(trainPredict)
#testPredict = scaler.inverse_transform(testPredict)


# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
testPredict = scaler.inverse_transform(testPredict)


pdb.set_trace()


trainY = scaler.inverse_transform([trainY])
testY = scaler.inverse_transform([testY])


trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))



print (trainPredict)

"""
scaler.inverse_transform(numpy.reshape (trainX.flatten(),(-1,1)))

scaler.inverse_transform(numpy.reshape (trainPredict.flatten(),(-1,1)))
"""

"""
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
"""


# In[ ]:



# 回復預測資料值為原始數據的規模
trainPredict = scaler.inverse_transform(trainPredict)
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
# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

