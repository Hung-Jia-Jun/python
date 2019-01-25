# -*- coding: UTF-8 -*-
import cv2
import ftplib
import os
import multiprocessing
import time
Username = " "
Password = " "
def upload(file):
	ftp = ftplib.FTP("files.000webhost.com")
	ftp.login(Username,Password)
	ext = os.path.splitext(file)[1]
	if ext in (".txt", ".htm", ".html"):
		ftp.storlines("STOR " + file, open(file))
	else:
		ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
	os.remove(FileName)
	print (FileName+" uploaded")





# 選擇第二隻攝影機
cap = cv2.VideoCapture(0)

while(True):
  # 從攝影機擷取一張影像
  ret, frame = cap.read()

  # 顯示圖片
  cv2.imshow('frame', frame)

  if cv2.waitKey(1) & 0xFF == ord('c'):
	FileName = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))+'.png'
	cv2.imwrite(FileName,frame)
	multiprocessing.Process(target=upload,args=(FileName,) ).start()
	

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
