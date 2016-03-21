#-*- coding: utf-8 -*-　
import cv2
from threading import Thread
import time
import sys,string
from Tkinter import *
import multiprocessing
from threading import *
import msvcrt
import numpy as np
Low=0
def ScrollBox(pipe):
	def resize(ev=None):
		Low=int(scale.get())
		Hight2=int(Hight.get())
		pipe.send([Low,Hight2])

	top = Tk()  #主窗口
	top.geometry('600x400')
	scale = Scale(top,from_=0,to=255,orient=HORIZONTAL,command=resize)
	scale.set(0)  #设置起始位置
	scale.pack(fill=X,expand=1)

	Hight = Scale(top,from_=0,to=255,orient=HORIZONTAL,command=resize)
	Hight.set(0)  #设置起始位置
	Hight.pack(fill=X,expand=1)
	mainloop()
	pass
def run_thread(pipe):
	def pipeRecv():
		while  True:
			Low2=pipe.recv()#重複迴圈接收發送的訊息
			Low   = Low2[0]
			Hight = Low2[1]
			print Low , Hight
			if msvcrt.kbhit():
				if ord(msvcrt.getch()) == 27:
					break
			pass
	cap = cv2.VideoCapture(0)
	Low2=pipe.recv()
	Low   = Low2[0]
	Hight = Low2[1]
	while True:
		ret0, frame = cap.read()#讀取攝影機的物件
		HSVColor  =  cv2.cvtColor (frame ,cv2.COLOR_BGR2HSV  )#轉換RGB變成HSV圖像

		lower_blue = np.array([111,Low,50])#低彩度設置[h,s,v]
		upper_blue = np.array([127,Hight,255])#高彩度設置[h,s,v]
		#Low=111 是藍色
		#Hight=127
		mask = cv2.inRange(HSVColor, lower_blue, upper_blue)#取出特徵值
		ret,thresh1=cv2.threshold(mask, 0 , 255 ,cv2.THRESH_BINARY)#二值化影像
		thresh1 = cv2.dilate(thresh1, None, iterations=2)
		#im2, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#cv2.drawContours(mask, contours, -1, (0,255,0), 3)
		cv2.imshow('frame', thresh1) 
		cv2.waitKey(5)
		Low2=pipe.recv()#重複迴圈接收發送的訊息
		Low   = Low2[0]
		Hight = Low2[1]
		if msvcrt.kbhit():
			if ord(msvcrt.getch()) == 27:
				pipeRecv()

				pass
		pass

	pass
	


if __name__ == '__main__':    
	pipe = multiprocessing.Pipe()
	t1 = multiprocessing.Process(target=ScrollBox, args=(pipe[0],))
	t2 = multiprocessing.Process(target=run_thread, args=(pipe[1],))
	t1.start()
	#raw_input().decode(sys.stdin.encoding)
	t2.start() 
