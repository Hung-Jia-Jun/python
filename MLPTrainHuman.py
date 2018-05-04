#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy
import pandas as pd
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten
import pdb
from keras.utils import np_utils
from keras.datasets import mnist
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session


import numpy as np
import cv2
from IPython.display import Image
from os import listdir
import pdb
from os.path import isfile, join
mypath="./TrainData"
TestDataPath="./TestData"

TestDatafiles = [f for f in listdir(TestDataPath) if isfile(join(TestDataPath, f))]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



Test_AllX_train_df=[]
X_test_df=[]

AllX_train_df=[]
# Load an color image in grayscale
for file in onlyfiles:
	if "png" in file:
		AasonLine=[]
		AasonLine.append(file.split("(")[0])
		img = cv2.imread(mypath+"/"+file,0)
		for ele in img:
			for ele2 in ele:
				AasonLine.append(ele2)
		AllX_train_df.append(AasonLine)
for file in TestDatafiles:
	if "png" in file:
		Test_AasonLine=[]
		Test_AasonLine.append(file.split("(")[0])
		img = cv2.imread(TestDataPath+"/"+file,0)
		for ele in img:
			for ele2 in ele:
				Test_AasonLine.append(ele2)
		X_test_df.append(Test_AasonLine)


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config = tf.ConfigProto(device_count = {'GPU': 1}) #0表示使用CPU，1则是GPU
#config.gpu_options.per_process_gpu_memory_fraction = 0.5
set_session(tf.Session(config=config))

def plot_image(image):
	fig=plt.gcf()
	fig.set_size_inches(2,2)
	plt.imshow(image,cmap='binary')
	plt.show()

def plot_images_labels_prediction(images,labels,prediction,idx,num=10): #image傳入圖片 labels=真實值 prediction=預測值 idx=開始顯示資料的index num=預設顯示10筆
	fig=plt.gcf()
	fig.set_size_inches(12,14)
	if num>25:num=25
	for i in range(0,num):
		ax=plt.subplot(5,5,1+i) #建立subgraph 子圖形為5行x5列
		ax.imshow(images[idx],cmap='binary') #畫出subgraph子圖形

		title='label='+str(labels[idx])
		if len(prediction)>0: #如果有傳入預測結果
			title+=',predict='+str(PredictionOnhottoInt(str(prediction[idx]))) #在title顯示預測結果
		ax.set_title(title, fontsize=10)
		ax.set_xticks([])
		ax.set_yticks([]) #設定不顯示刻度
		idx+=1 #讀取下一筆
	plt.show()

def PredictionOnhottoInt(prediction):
	pdb.set_trace()
	Predictionli=list(prediction[1:-1].split(" "))
	try:
		Predictionli.remove("") #清空空值
	except:
		pass
	PredictionInt=0
	num=0
	for ele in Predictionli:
		if ele.replace(" ","")=="1":
			return num
		num+=1
	return 3


def show_train_history(train_history,train,validation):
	plt.plot(train_history.history[train])
	plt.plot(train_history.history[validation])
	plt.title('Train History')
	plt.ylabel(train)
	plt.xlabel('Epoch')
	plt.legend(['train','validation'],loc="upper left")
	plt.show()


def PreprocessData(RawData):
	TotalRaw=[]
	RawDataOnehot=[]
	for ele in RawData:
		for ele2 in ele:
			RawDataOnehot.append(int(ele2)/255)
		TotalRaw.append(RawDataOnehot)

	return TotalRaw
numpy.random.seed(10)


X_train_df=AllX_train_df



#(X_train_image,y_train_label),(X_test_image,y_test_label)=mnist.load_data()



#train label
y_train_label=[]
for ele in X_train_df:
	y_train_label.append(ele[0])



#驗證Label
y_test_label=[]
for ele in X_test_df:
	y_test_label.append(ele[0])


#train列
X_Train=X_train_df
#驗證資料
X_Test=X_test_df

#X_Train=X_train_image.reshape(60000,784).astype('float32') #轉換成一維的向量
#X_Test=X_test_image.reshape(10000,784).astype('float32') #轉換成一維的向量

#圖像
X_Train_normalize=PreprocessData(X_Train)
X_Test_normalize=PreprocessData(X_Test)

#圖像真實值 onehot處理  1=1000000000  2=0100000000  5=0000500000
y_TrainOneHot=np_utils.to_categorical(y_train_label)
y_TestOneHot=np_utils.to_categorical(y_test_label)

model=Sequential()
#輸入層
#704*480
#units=1000 隱藏層1000神經元
#input_dim=337920 輸入層 337920個
model.add(Dense(units=10,
				input_dim=8785946,
				kernel_initializer="uniform",
				activation='relu'))

#model.add(Dropout(0.5)) #隨機捨棄50%的神經節點


#隱藏層
model.add(Dense(units=10,
				input_dim=8785946,
				kernel_initializer="uniform",
				activation='relu'))
#model.add(Dropout(0.5)) #隨機捨棄50%的神經節點

#輸出層
#units=10 10個神經元 因為是0-9個數字
#kernel_initializer="normal" 使用 normal distribution 常態分佈亂數 自動初始化 weight 和 bias
#model.add(Flatten())
model.add(Dense(units=2,
				kernel_initializer="normal",
				activation='softmax'))

#編譯模型
model.compile(loss='categorical_crossentropy',
				optimizer="adam",
				metrics=['accuracy'])
print(model.summary())
#開始訓練
#validation_split=0.2 Keras會自動將資料分成80% 訓練資料  20%測試資料
#verbose=2 顯示訓練過程


train_history=model.fit(x=np.array(X_Train_normalize),
						y=np.array(y_TrainOneHot),
						validation_split=0.1,
						epochs=50,
						batch_size=200,verbose=2)


#acc 訓練準確率 val_acc驗證的準確率
show_train_history(train_history,'acc','val_acc')

#show_train_history(train_history,'loss','val_loss')

#評估準確度
scores=model.evaluate(x=np.array(X_Train_normalize),y=np.array(y_TrainOneHot),)[1]
print (scores)




prediction=model.predict(np.array(X_Train_normalize))
pdb.set_trace()
#使用模型進行預測
#prediction=model.predict(np.array(X_Train_normalize).reshape((8785946,-1))  )


for ele in prediction:
	result=PredictionOnhottoInt(str(ele))
	open("Req2.txt","a").write((str(result).replace(" ","")+"\n"))
#plot_images_labels_prediction(X_train_image,y_train_label,prediction,idx=30)
