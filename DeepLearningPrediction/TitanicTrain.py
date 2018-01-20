import numpy
import pandas as pd
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense,Dropout
import pdb
def PreprocessData(raw_df):
	df=raw_df.drop(['Name'],axis=1)
	age_mean=df['Age'].mean() #填入年齡欄位的平均值
	df['Age']=df['Age'].fillna(age_mean)#填入到空白處

	fare_mean=df['Fare'].mean() #填入年齡欄位的平均值
	df['Fare']=df['Fare'].fillna(age_mean)#填入到空白處

	df['Sex']=df['Sex'].map({'female':0,'male':1}).astype(int)
	x_OneHot_df=pd.get_dummies(data=df,columns=['Embarked'])

	ndarry=x_OneHot_df.values
	Features=ndarry[:,1:]
	Label=ndarry[:,0]

	minmax_scale=preprocessing.MinMaxScaler(feature_range=(0,1))#資料標準化
	scaleFeatures=minmax_scale.fit_transform(Features)

	return scaleFeatures,Label

numpy.random.seed(10)
all_df=pd.read_csv("train.csv")
cols=['Survived','Name','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
all_df=all_df[cols]

msk=numpy.random.rand(len(all_df))<0.8
train_df=all_df[msk]
test_df=all_df[~msk]


Test_df=pd.read_csv("test.csv")
cols=['Survived','Name','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
Test_df=Test_df[cols]



train_Features,train_Label=PreprocessData(train_df)
test_Features,test_Label=PreprocessData(train_df)

all_Features,Label=PreprocessData(Test_df)
model=Sequential()
#輸入層
model.add(Dense(units=40,
				input_dim=9,
				kernel_initializer="uniform",
				activation='relu'))

#隱藏層
model.add(Dense(units=3000,
				kernel_initializer="uniform",
				activation='relu'))

#輸出層
model.add(Dense(units=1,
				input_dim=9,
				kernel_initializer="uniform",
				activation='sigmoid'))
model.compile(loss='binary_crossentropy',
				optimizer="adam",
				metrics=['accuracy'])
train_history=model.fit(x=train_Features,
						y=train_Label,
						validation_split=0.1,
						epochs=30,
						batch_size=30,verbose=2)

#評估準確度
scores=model.evaluate(x=test_Features,
						y=test_Label,)

#預測測試集
all_probability=model.predict(all_Features)
print (all_probability[-2:])
print (all_df[-2:])
writeLog=[]
for ele in all_probability:
	if float(ele[0])>0.8:
		writeLog.append(1)
	else:
		writeLog.append(0)
open("Req.txt","w").write(''.join(str(writeLog)))
