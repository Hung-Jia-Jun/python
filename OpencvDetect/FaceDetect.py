#-*- coding: utf-8 -*-　
import cv2
import sys
import time
import serial
import pdb
import os
import random
USBPORT="COM"+str(raw_input("USB Port: "))
ser =serial.Serial(str(USBPORT),9600) #開啟USBPort



Test=False 
if Test==True:
	while True:
		ser.write("C") #clear	
		ser.write(str(random.randint(5,8))+str(random.randint(5,8))+"1")
		time.sleep(0.2)
		#print (eleY,eleX)
pdb.set_trace()
			
LedPositionX=0
LedPositionY=0

cascPath = sys.argv[1]
#cascPath=os.getcwd()+"haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture(0)


cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

while True:
	# Capture frame-by-frame
	before = time.time()
	#frame =cv2.imread("C:\\Python27\\Scripts\\LedArray\\ScreenShot\\S__18358313.jpg")  #read img
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=10,
		minSize=(30, 30),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	after = time.time()
	#print "Found {0} faces!, fps= {1}".format(len(faces), round(1/(after-before), 1))
	# Draw a rectangle around the faces
	if len(faces)==0:
		ser.write(str(random.randint(5,8))+str(random.randint(5,8))+"1")
		ser.write("C") #clear
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		#print (x, y),(x+w, y+h)
		cv2.circle(frame,((x+(x+w))/2, (y+(y+h))/2),10,(255,255,255),-11)
		LedPositionX=((x+(x+w))/200)
		LedPositionY=((y+(y+h))/200)
		LedPositionX=str(LedPositionX)
		LedPositionY=str(LedPositionY)
		ser.write("C") #clear
		time.sleep(0.1)
		print "Face Location: ",LedPositionX,LedPositionY
		#print "Face Location Base: ",((x+(x+w))/2),((y+(y+h))/2)
		#ser.write(str(random.randint(5,8))+str(random.randint(5,8))+"1")
		ser.write(LedPositionY+LedPositionX+"1")      # write a string
	# Display the resulting frame
	cv2.imshow("preview", frame)

	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
