#-*- coding: utf-8 -*-　
import cv2

import time
import sys,string
import multiprocessing

import msvcrt
import numpy as np
import pdb
#Low=0
# 当调节滑块时，调用这个函数。这个没有使用到
def do_nothing(x):
    pass

#cv2.namedWindow('image') #開啟設定窗口

# 创建滑块,注册回调函数
cv2.createTrackbar('LowerH','image',0,255,do_nothing)
cv2.createTrackbar('HightH','image',0,255,do_nothing)

cv2.createTrackbar('LowerS','image',0,255,do_nothing)
cv2.createTrackbar('HightS','image',0,255,do_nothing)

cv2.createTrackbar('LowerV','image',0,255,do_nothing)
cv2.createTrackbar('HightV','image',0,255,do_nothing)
def PointTakeing(frame):#分離三點
	HSVColor  =  cv2.cvtColor (frame,cv2.COLOR_BGR2HSV)#轉換RGB變成HSV圖像
	#----A點
	HSVlower = np.array([2,0,0])#低彩度設置[h,s,v]
	HSVupper = np.array([32,255,255])#高彩度設置[h,s,v]
	mask = cv2.inRange(HSVColor, HSVlower, HSVupper)#取出特徵值
	ret,threshA=cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV)#二值化影像
	image,contours,hierarchy = cv2.findContours(threshA,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  
	cnt=contours[0]
	cv2.drawContours(frame,cnt,0,(0,0,255),4) #繪製點在球上
	font_1_X=cnt[0,0,0]#從座標陣列cnt提取出X來給顯示點1上的數字座標
	font_1_Y=cnt[0,0,1]#從座標陣列cnt提取出Y來給顯示點1上的數字座標
	str_Point_1='C.('+str(font_1_X)+','+str(font_1_Y)+')'
	cv2.putText(frame, str_Point_1 ,(font_1_X,font_1_Y), 0 , 0.5 , ( 0 , 0 , 255 ), 1 )
	#----A點

	#----B點
	HSVlower = np.array([44,0,0])#低彩度設置[h,s,v]
	HSVupper = np.array([56,255,255])#高彩度設置[h,s,v]
	mask = cv2.inRange(HSVColor, HSVlower, HSVupper)#取出特徵值
	ret,threshB=cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV)#二值化影像
	image,contours,hierarchy = cv2.findContours(threshB,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  
	cnt=contours[0]
	cv2.drawContours(frame,cnt,0,(0,0,255),4) #繪製點在球上
	font_2_X=cnt[0,0,0]#從座標陣列cnt1提取出X來給顯示點2上的數字座標
	font_2_Y=cnt[0,0,1]#從座標陣列cnt1提取出Y來給顯示點2上的數字座標
	str_Point_2='B.('+str(font_2_X)+','+str(font_2_Y)+')'
	cv2.putText(frame, str_Point_2 ,(font_2_X,font_2_Y), 0 , 0.5 , ( 0 , 0 , 255 ), 1 )
	#----B點

	#----C點
	HSVlower = np.array([89,0,0])#低彩度設置[h,s,v]
	HSVupper = np.array([164,255,255])#高彩度設置[h,s,v]
	mask = cv2.inRange(HSVColor, HSVlower, HSVupper)#取出特徵值
	ret,threshC=cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV)#二值化影像
	image,contours,hierarchy = cv2.findContours(threshC,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  
	cnt=contours[0]
	cv2.drawContours(frame,cnt,0,(0,0,255),4) #繪製點在球上
	font_3_X=cnt[0,0,0]#從座標陣列cnt2提取出X來給顯示點3上的數字座標
	font_3_Y=cnt[0,0,1]#從座標陣列cnt2提取出Y來給顯示點3上的數字座標
	str_Point_3='A.('+str(font_3_X)+','+str(font_3_Y)+')'
	cv2.putText(frame, str_Point_3 ,(font_3_X,font_3_Y), 0 , 0.5 , ( 0 , 0 , 255 ), 1 )
	return font_1_X,font_1_Y,font_2_X,font_2_Y,font_3_X,font_3_Y,
	#----C點
	pass
def Liner(ReadX,ReadY,ReadZ,P2_Z,frame):#處理直線方程式的函式，核心演算法別動阿～

	ReadX=ReadX*-1+600#X軸
		
	ReadY=(ReadY*-1+1500)/3#Y軸

	Xlimit=(ReadY-62)/0.6#y=0.6x+62 直線方程式
	Xlimit=round(Xlimit)
	Xlimit=str(Xlimit)
	Xlimit=Xlimit[0:3]#限制整數，不可以小數點
	Xlimit=int(Xlimit)
	if ReadX>Xlimit:
		ReadX=Xlimit
	if ReadY<333:
		ReadY=333



	Zhight= ReadY-P2_Z#Z軸高度為獲取到的Y軸減去輸入的Y軸得出
	WeightY=ReadY/480.0
	
	Hight= (Zhight*-WeightY)+150
	intHight=int(Hight)
	strHight=str(Hight)
	print intHight
	cv2.line(frame,(ReadX,ReadY),(ReadX,ReadY), (0,0,255) , 5 )
	cv2.line(frame,(ReadX,ReadY),(ReadX,ReadY-intHight), (0,0,255) , 5 )
	return intHight
	pass
def detailTxt():#處理文字檔裡面的X,Y值
#-----辨識後的Z軸
	A_Z_Detail= open('C:\\A_Z_Detail.txt', 'w')
	B_Z_Detail= open('C:\\B_Z_Detail.txt', 'w')
	C_Z_Detail= open('C:\\C_Z_Detail.txt', 'w')
#-----辨識後的Z軸

#---------A光球
	Readfile_A_X = open('C:\\1avi_A_X.txt', 'r')
	Readfile_A_Y = open('C:\\1avi_A_Y.txt', 'r')
	Readfile_A_Z = open('C:\\1avi_A_Z.txt', 'r')
#---------A光球

#---------B光球
	Readfile_B_X = open('C:\\1avi_B_X.txt', 'r')
	Readfile_B_Y = open('C:\\1avi_B_Y.txt', 'r')
	Readfile_B_Z = open('C:\\1avi_B_Z.txt', 'r')
#---------B光球

#---------C光球
	Readfile_C_X = open('C:\\1avi_C_X.txt', 'r')
	Readfile_C_Y = open('C:\\1avi_C_Y.txt', 'r')
	Readfile_C_Z = open('C:\\1avi_C_Z.txt', 'r')
#---------C光球
	WriteLog = open('C:\\Log.txt', 'w')
	cap = cv2.VideoCapture("c03.avi")#讀取2.avi
	while True:
		ret0, frame = cap.read()#讀取攝影機的物件
		TakeingResaul= PointTakeing(frame)
		font_1_Y=TakeingResaul[1]
		font_2_Y=TakeingResaul[3]
		font_3_Y=TakeingResaul[5]
		"""
		LowerH = 0#cv2.getTrackbarPos('LowerH','image')
		HightH = 0#cv2.getTrackbarPos('HightH','image')

		LowerS = 0#cv2.getTrackbarPos('LowerS','image')
		HightS = 255#cv2.getTrackbarPos('HightS','image')

		LowerV = 0#cv2.getTrackbarPos('LowerV','image')
		HightV = 255#cv2.getTrackbarPos('HightV','image')

		HSVlower = np.array([LowerH,LowerS,LowerV])#低彩度設置[h,s,v]
		HSVupper = np.array([HightH,HightS,HightV])#高彩度設置[h,s,v]
		"""

		txt_Readfile_A_X = Readfile_A_X.readline()#逐行讀取文字檔內容光球的X軸
		int_Readfile_A_X=int(txt_Readfile_A_X)#字串轉int的X軸
			
		txt_Readfile_A_Y = Readfile_A_Y.readline()#逐行讀取文字檔內容光球的Y軸
		int_Readfile_A_Y=int(txt_Readfile_A_Y)#字串轉int的Y軸

		txt_Readfile_A_Z = Readfile_A_Z.readline()#逐行讀取文字檔內容光球的Z軸
		int_Readfile_A_Z=int(txt_Readfile_A_Z)#字串轉int的Z軸


		txt_Readfile_B_X= Readfile_B_X.readline()#逐行讀取文字檔內容光球的X軸
		int_Readfile_B_X= int(txt_Readfile_B_X)#字串轉int的X軸

		txt_Readfile_B_Y= Readfile_B_Y.readline()#逐行讀取文字檔內容光球的Y軸
		int_Readfile_B_Y =int(txt_Readfile_B_Y)#字串轉int的Y軸

		txt_Readfile_B_Z= Readfile_B_Z.readline()#逐行讀取文字檔內容光球的Z軸
		int_Readfile_B_Z=int(txt_Readfile_B_Z)#字串轉int的Z軸


		txt_Readfile_C_X= Readfile_C_X.readline()#逐行讀取文字檔內容光球的X軸
		int_Readfile_C_X=int(txt_Readfile_C_X)#字串轉int的X軸

		txt_Readfile_C_Y= Readfile_C_Y.readline()#逐行讀取文字檔內容光球的Y軸
		int_Readfile_C_Y=int(txt_Readfile_C_Y)#字串轉int的Y軸

		txt_Readfile_C_Z= Readfile_C_Z.readline()#逐行讀取文字檔內容光球的Z軸
		int_Readfile_C_Z=int(txt_Readfile_C_Z)#字串轉int的Z軸



		A_Z_strHight=Liner(int_Readfile_A_X ,int_Readfile_A_Y ,int_Readfile_A_Z ,font_1_Y,frame)#A點的座標(X,Y,Z,跟C相機的1號光球Z軸相減的數值,要畫在上面的Frame)
		A_Z_strHight=str(A_Z_strHight)
		A_Z_Detail.write(A_Z_strHight)
		A_Z_Detail.write("\n")#換行


		B_Z_strHight=Liner(int_Readfile_B_X ,int_Readfile_B_Y ,int_Readfile_B_Z ,font_2_Y,frame)#B點的座標(X,Y,Z,跟C相機的2號光球Z軸相減的數值,要畫在上面的Frame)
		B_Z_strHight=str(B_Z_strHight)
		B_Z_Detail.write(B_Z_strHight)
		B_Z_Detail.write("\n")#換行

		C_Z_strHight=Liner(int_Readfile_C_X ,int_Readfile_C_Y ,int_Readfile_C_Z ,font_3_Y,frame)#C點的座標(X,Y,Z,跟C相機的3號光球Z軸相減的數值,要畫在上面的Frame)
		C_Z_strHight=C_Z_strHight+100
		C_Z_strHight=str(C_Z_strHight)
		C_Z_Detail.write(C_Z_strHight)
		C_Z_Detail.write("\n")#換行



		cv2.imshow('DetailPostion', frame) 
		cv2.waitKey(10)
		pass

def run_thread(): #A相機
	cap = cv2.VideoCapture("c01.avi")
	file = open('C:\\1avi_A_Y.txt','w')
	file_B_Y = open('C:\\1avi_B_Y.txt','w')
	file_C_Y = open('C:\\1avi_C_Y.txt','w')
	while True:
		ret0, frame = cap.read()#讀取攝影機的物件
		"""     
		如果要重複播放影片的話就開啟這段程式碼
		因為有時候會用到debug影像
		要找到影像的特徵點
		所以要一直重複播放
		如果未來不需要用影片算座標的話就可以刪掉這段了
		"""
		"""
		try:
			HSVColor  =  cv2.cvtColor (frame ,cv2.COLOR_BGR2HSV  )#轉換RGB變成HSV圖像
			pass
		except :
			cap = cv2.VideoCapture("1.avi")
			ret0, frame = cap.read()#讀取攝影機的物件
			HSVColor  =  cv2.cvtColor (frame ,cv2.COLOR_BGR2HSV  )#轉換RGB變成HSV圖像
			pass
		"""
		TakeingResaul= PointTakeing(frame)#依序推入需要計算的XY值，並且依照位置獲取指定的字元
		font_1_X=TakeingResaul[0]
		font_2_X=TakeingResaul[2]
		font_3_X=TakeingResaul[4]

		#1.avi影片的A點位置
		GlobalY=str(font_1_X)#把X軸左右交給A處理，並寫到世界座標的Y軸去
		file.write(GlobalY)#寫入Txt
		file.write("\n")#換行
		 
		#1.avi影片的B點位置
		Global_B_Y=str(font_2_X)
		file_B_Y.write(Global_B_Y)
		file_B_Y.write("\n")#換行

		#1.avi影片的C點X軸位置
		Global_C_Y=str(font_3_X)
		file_C_Y.write(Global_C_Y)
		file_C_Y.write("\n")#換行

		cv2.imshow('X', frame) 
		cv2.waitKey(5)
		pass

	pass
	
def run_thread2(): #B相機
	cap = cv2.VideoCapture("c02.avi")#讀取2.avi  
	file = open('C:\\1avi_A_X.txt','w')
	file_B_X = open('C:\\1avi_B_X.txt','w')
	file_C_X = open('C:\\1avi_C_X.txt','w')

	while True:
		ret0, frame = cap.read()#讀取攝影機的物件
		TakeingResaul= PointTakeing(frame)
		font_1_X=TakeingResaul[0]
		font_2_X=TakeingResaul[2]
		font_3_X=TakeingResaul[4]


		GlobalX=str(font_1_X)#會這麼做的原因是因為物體會上下跳動，唯有X值左右是不會變的
		file.write(GlobalX)#寫入Txt
		file.write("\n")#換行

		#2.avi影片的B點位置
		Global_B_X=str(font_2_X)
		file_B_X.write(Global_B_X)
		file_B_X.write("\n")#換行

		#2.avi影片的C點X軸位置
		Global_C_X=str(font_3_X)
		file_C_X.write(Global_C_X)
		file_C_X.write("\n")#換行
		cv2.imshow('Y', frame) 
		 
		cv2.waitKey(5)
		pass
	pass


if __name__ == '__main__':   
	p1 = multiprocessing.Process(target=run_thread )
	p2 = multiprocessing.Process(target=run_thread2)
	p3 = multiprocessing.Process(target=detailTxt)
	#p4 = multiprocessing.Process(target=detailTxt)


	#pdb.set_trace()
	#p1.start()
	#p2.start()
	#raw_input()
	p3.start()
	
	#detailTxt()
