#-*- coding: utf-8 -*-　
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2,pdb
import cv2
import sys
import time
import serial
import pdb
import os

#USBPORT="COM"+str(raw_input("USB Port: "))
USBPORT="COM3"
ser =serial.Serial(str(USBPORT),9600) #開啟USBPort

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cascPath = os.getcwd()+"/haarcascade_frontalface_default.xml"
#cascPath=os.getcwd()+"haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


LedPositionX=0
LedPositionY=0

cap = cv2.VideoCapture(0)


cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

while True:
	ret, image = cap.read()


	ret, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=10,
		minSize=(30, 30),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)





	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),padding=(8, 8), scale=1.05)

	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)


	if len(pick)==0:
		for (x, y, w, h) in faces: #頭部辨識
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			#print (x, y),(x+w, y+h)
			cv2.circle(image,((x+(x+w))/2, (y+(y+h))/2),10,(255,255,255),-11)
			LedPositionX=((x+(x+w))/200)
			LedPositionY=((y+(y+h))/200)
			LedPositionX=str(LedPositionX)
			LedPositionY=str(LedPositionY)


			#print "Face Location: ",LedPositionX,LedPositionY
			ser.write(LedPositionY+LedPositionX+"1") 
			ser.write("C") #clear
			print "Face Location: ",0,0


	for (xA, yA, xB, yB) in pick: #足部辨識
		LedPositionX=(((xA+xB)/2)/200)
		LedPositionY=(yB/200)
		LedPositionX=str(LedPositionX)
		LedPositionY=str(LedPositionY)
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
		cv2.circle(image,((xA+xB)/2, yB),10,(255,255,255),-11)
		print LedPositionX+":"+LedPositionY


	


	cv2.imshow("preview", image)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
#except: #restart 
	#os.system("python "+os.getcwd()+"/HumanDetect.py "+os.getcwd()+"/haarcascade_frontalface_default.xml")
cap.release()
cv2.destroyAllWindows()
