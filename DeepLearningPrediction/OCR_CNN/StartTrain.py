
# coding: utf-8

# In[19]:

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
import cv2
import os
import os.path
import xlrd
from sklearn import svm
import numpy as np
import pdb

#Read CSV

import csv

csvfile = open('GenPics/lables.csv')
reader = csv.reader(csvfile)

lables = []
for line in reader:
	try:
		tmp = [line[0],line[1]]
		#print tmp
		lables.append(tmp)
	except:
		pass

csvfile.close() 


X = []
y = []
picnum = len(lables)
print ("picnum : ",picnum)
for i in range(0,picnum):
		img = cv2.imread("GenPics/" + lables[i][0] + '.jpg', cv2.IMREAD_GRAYSCALE)
		X.append(img)    
		y.append(lables[i][1])



#定義類別輸出神經元對應到的英文字母與數字
labeldict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,
						 'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,
						 'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,
						 '0':26,
						 '1':27,
						 '2':28,
						 '3':29,
						 '4':30,
						 '5':31,
						 '6':32,
						 '7':33,
						 '8':34,
						 '9':35}
num_classes = 36

X = np.array(X)

for i in range(len(y)):
	c0 = keras.utils.to_categorical(labeldict[y[i][0]], num_classes)
	c1 = keras.utils.to_categorical(labeldict[y[i][1]], num_classes)
	c2 = keras.utils.to_categorical(labeldict[y[i][2]], num_classes)
	c3 = keras.utils.to_categorical(labeldict[y[i][3]], num_classes)
	c = np.concatenate((c0,c1,c2,c3),axis=None)
	y[i] = c

y = np.array(y)




batch_size = 25

#訓練次數
epochs = 200

img_rows, img_cols = 20, 80

x_train = X[:8000]
y_train = y[:8000]
x_test = X[8000:]
y_test = y[8000:]


#重新設定圖片的cols
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

x_train = 255 - x_train
x_test = 255 - x_test
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255


#定義模型
model = Sequential()

model.add(Conv2D(32, kernel_size=(5, 9),activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 4)))

model.add(Conv2D(16, kernel_size=(5, 7), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 3)))

model.add(Flatten())

model.add(Dense(num_classes*4, activation='sigmoid'))

model.compile(loss=keras.losses.binary_crossentropy,
							optimizer=keras.optimizers.Adadelta(),
							metrics=['accuracy'])




#開始訓練
#將監督資料輸入後開始訓練
model.fit(x_train, y_train,
					batch_size=batch_size,
					epochs=epochs,
					verbose=1,
					validation_data=(x_test, y_test))


#儲存模型
model.save('Model/my_model.h5')


#評估準確度
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# In[35]:

pred = model.predict(x_test,batch_size = 25)


# In[36]:

outdict = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

Resultlables=[]
correct_num = 0
for i in range(pred.shape[0]):
	try:
		c0 = outdict[np.argmax(pred[i][:36])]
		c1 = outdict[np.argmax(pred[i][36:36*2])]
		c2 = outdict[np.argmax(pred[i][36*2:36*3])]
		c3 = outdict[np.argmax(pred[i][36*3:])]
		captchaImg = c0+c1+c2+c3
		#print c,lables[8000+i][1]
		Resultlables.append((str(8000+i),captchaImg))
		if captchaImg == lables[8000+i][1]:
			#每成功一次就在成功率的基數下+1，這樣才能估算成功率
			correct_num = correct_num + 1
	except:
		pass
#統計正確率 0-1.0
print ("Test Whole Accurate : ", float(correct_num)/len(pred))


import csv
csvfile = open('GenPics/Result.csv', 'w')
writer = csv.writer(csvfile)
writer.writerows(Resultlables)
csvfile.close()
