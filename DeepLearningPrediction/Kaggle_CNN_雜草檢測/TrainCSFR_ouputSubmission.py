
# coding: utf-8

# In[19]:
import keras
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.core import Dense, Activation
from keras.layers import Conv2D, MaxPooling2D,Convolution2D
from keras import backend as K
import numpy as np
import cv2
import os
import os.path
import xlrd
from sklearn import svm
import numpy as np
import pdb
from tqdm import tqdm
from keras.layers import BatchNormalization
#Read CSV
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

import csv
import tensorflow as tf

from keras.backend.tensorflow_backend import set_session

#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#config.gpu_options.per_process_gpu_memory_fraction = 0.7
#set_session(tf.Session(config=config))

def show_train_history(train_history,train,validation):
	plt.plot(train_history.history[train])
	plt.plot(train_history.history[validation])
	plt.title('Train History')
	plt.ylabel(train)
	plt.xlabel('Epoch')
	plt.legend(['train','validation'],loc="upper left")
	plt.show()

X = []
y = []


#因為要讓所有圖片大小一致
#圖片Size  Hight資訊
imgSizeHight=[]

#圖片Size  Width資訊
imgSizeWidth=[]


#求出本圖集中最大的圖片寬高


#不知道圖片裡最大的寬高時，打開這邊來運行搜尋最大圖片的工作
"""
for Filename in tqdm(os.listdir('all/train/TotalTrainImage')):
	img = cv2.imread("all/train/TotalTrainImage/" + Filename, cv2.IMREAD_GRAYSCALE)
	
	#該圖片的寬高
	Hight,Width=img.shape
	imgSizeHight.append(Hight)
	imgSizeWidth.append(Width)


Max_Hight=max(imgSizeHight)
Max_Width=max(imgSizeWidth)
"""

#使用完後釋放記憶體位置
imgSizeHight=[]
imgSizeWidth=[]

#有確定加入訓練集的list 用於評估正確率
FilenameLi=[]

i=0

#欲縮放圖片大小
Max_Width=100
Max_Hight=100

#圖片預處理
def ImagePreEdit(Filename):
	#欲縮放圖片大小
	Max_Width=100
	Max_Hight=100


	img = cv2.imread(Filename)
	img=cv2.resize(img, (Max_Width, Max_Hight), interpolation=cv2.INTER_CUBIC)


	#將閥值組合成np array
	HSVlower = np.array([25, 40, 50],dtype='float64')
	HSVupper = np.array([75, 255, 255],dtype='float64')

	#HSVlower = np.array([LowerH,LowerS,LowerV],dtype='float64')#低彩度設置[h,s,v]
	#HSVupper = np.array([HightH,HightS,HightV],dtype='float64')#高彩度設置[h,s,v]

	#將RGB轉換成HSV色彩空間
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	#設定mask 去抓取葉子的顏色
	mask = cv2.inRange(hsv, HSVlower, HSVupper)
	res = cv2.bitwise_and(img,img, mask= mask)
	#cv2.imshow("mask",res)

	#cv2.waitKey (10)
	#將mask 後的圖片轉換成黑白兩個通道的圖片
	
	#0度
	Gray_res=cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	#90
	res1=np.rot90(res)
	Gray_res1=cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)

	#180
	res2=np.rot90(res,2)
	Gray_res2=cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

	#270
	res3=np.rot90(res,3)
	Gray_res3=cv2.cvtColor(res3, cv2.COLOR_BGR2GRAY)

	"""
	cv2.imshow("mask",res)
	cv2.imshow("mask1",res1)
	cv2.imshow("mask2",res2)
	cv2.imshow("mask3",res3)

	cv2.waitKey (10)
	pdb.set_trace()
	"""
	#四種角度的圖片
	return Gray_res,Gray_res1,Gray_res2,Gray_res3


#測試圖集
Test_X=[]
"""
#重新調整大小後塞入圖片陣列
for Filename in tqdm(os.listdir('all/train/TotalTrainImage')):
	#訓練集
	Train_Gray_res=ImagePreEdit("all/train/TotalTrainImage/" + Filename)
	#因為轉四個角度，所以label都要加四個
	#將更改的照片放進list
	X.append(Train_Gray_res[0])
	#for ele in Train_Gray_res:
	#	X.append(ele)   

	#for i in range(4):
	y.append(Filename.split("_")[0])
	FilenameLi.append(Filename)
	cv2.destroyAllWindows()
	i+=1
"""
#重新調整大小後塞入圖片陣列
for Filename in tqdm(os.listdir('all/TestData/test/')):
	#測試集
	Test_Gray_res=ImagePreEdit('all/TestData/test/' + Filename)
	X.append(Test_Gray_res[0])
	#將檔案名稱儲存起來
	FilenameLi.append(Filename)

	#新增Label 
	y.append('Black-grass')
	
	#將更改的照片放進list
	Test_X.append(Test_Gray_res[0])    
#定義類別輸出神經元對應到的英文字母與數字
labeldict = {   "Black-grass":0,
				"Charlock":1,
				"Cleavers":2,
				"CommonChickweed":3,
				"Commonwheat":4,
				"FatHen":5,
				"LooseSilky-bent":6,
				"Maize":7,
				"ScentlessMayweed":8,
				"ShepherdsPurse":9,
				"Small-floweredCranesbill":10,
				"Sugarbeet":11}
num_classes = 12


for i in range(len(y)):
	c0 = keras.utils.to_categorical(labeldict[y[i]], num_classes)
	c = np.concatenate((c0),axis=None)
	y[i] = c

#轉化為numpy的多維陣列
X = np.array(X)
Test_X=np.array(Test_X)
y = np.array(y)


#梯度下降採樣率
batch_size = 5

#訓練集與測試集分割閥值
SplitLimit=int(len(X)/2)

#訓練集
x_train = X
y_train = y

#驗證集
#x_test = X[SplitLimit:]

#比賽的測試集
x_test = Test_X

y_test = y[SplitLimit:]

#重新設定圖片的cols
x_train = x_train.reshape(x_train.shape[0], Max_Width, Max_Hight,1)
x_test = x_test.reshape(x_test.shape[0], Max_Width, Max_Hight,1)
input_shape = (Max_Width, Max_Hight,1)

x_train = 255 - x_train
x_test = 255 - x_test
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

pdb.set_trace()
#載入模型
model = load_model('my_model.h5')
#產生預測度
pred = model.predict(x_test,batch_size = batch_size)

#model.save('my_model.h5')   # HDF5 file, you have to pip3 install h5py if don't have it

# In[36]:


Resultlables=[]
def GetPredScore(pred):
	global FilenameLi,Resultlables
	Resultlables=[]
	correct_num = 0
	outdict = [
	"Black-grass",
	"Charlock",
	"Cleavers",
	"Common Chickweed",
	"Common wheat",
	"Fat Hen",
	"Loose Silky-bent",
	"Maize",
	"Scentless Mayweed",
	"Shepherds Purse",  
	"Small-flowered Cranesbill",
	"Sugar beet"]

	Resultlables.append(("file","species"))
	for i in range(pred.shape[0]):
		try:
			captchaImg = outdict[np.argmax(pred[i])]
			Resultlables.append((FilenameLi[i],captchaImg))
		except:
			pass

	#統計正確率 0-1.0
	print ("Test Whole Accurate : ", (float(correct_num)/len(pred))*100)
GetPredScore(pred)
pdb.set_trace()



import csv
csvfile = open('submission.csv', 'w')
writer = csv.writer(csvfile)
writer.writerows(Resultlables)
csvfile.close()
