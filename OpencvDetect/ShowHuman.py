#!/usr/bin/env python

'''
example to detect upright people in images using HOG features
Usage:
	peopledetect.py <image_names>
Press any key to continue, ESC to stop.
'''

# Python 2/3 compatibility
from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2 as cv
import pdb

def inside(r, q):
	rx, ry, rw, rh = r
	qx, qy, qw, qh = q
	return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 3):
	global frame,crop_x,crop_y
	if len(rects)==0:
		cv.imwrite('C:\\ProgramData\\Anaconda3\\Scripts\\OpenCVDetect\\FindedHuman\\'+str(frame)+'_false.png',img)
	for x, y, w, h in rects:
		pad_w, pad_h = int(0.15*w), int(0.05*h)
		if x>50 and x<100:
		#	if y>200:
			print (x, y)
			x=crop_x+x
			y=crop_y+y
			cv.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
			print('found')
			cv.imwrite('C:\\ProgramData\\Anaconda3\\Scripts\\OpenCVDetect\\FindedHuman\\'+str(frame)+'_true.png',img)

frame=0
JumpScream=0
crop_y=100
crop_x=200
if __name__ == '__main__':
	import sys
	from glob import glob
	import itertools as it

	hog = cv.HOGDescriptor()
	hog.setSVMDetector( cv.HOGDescriptor_getDefaultPeopleDetector() )

	#default = [''] if len(sys.argv[1:]) == 0 else []
	cap=cv.VideoCapture('C:\\ProgramData\\Anaconda3\\Scripts\\OpenCVDetect\\Pic\\20180416_172000_CH12_01.avi')
	
	while True:
		try:
			ret,img = cap.read()
			#img=cv.imread('C:\\ProgramData\\Anaconda3\\Scripts\\OpenCVDetect\\Pic\\7.png')
		except:
			print('loading error')


		
		frame+=1
		JumpScream+=1
		if JumpScream>2800:
			
			h=650
			w=470
			crop_img = img[crop_y:crop_y+h, crop_x:crop_x+w]
			try:
				found, w = hog.detectMultiScale(crop_img, winStride=(3,3), padding=(8,8), scale=1.05)


				#found_filtered = []
				#for ri, r in enumerate(found):
				#	for qi, q in enumerate(found):
				#		if ri != qi and inside(r, q):
				#			break
				#	else:
				#		found_filtered.append(r)

				found = np.array([[x, y, x + w, y + h] for (x, y, w, h) in found])
				found = non_max_suppression(found, probs=None, overlapThresh=0.65)
				draw_detections(img, found)
				#draw_detections(crop_img, found_filtered, 3)


				cv.imshow('img', img)
				#break
				if cv.waitKey(1) & 0xFF == ord("q"):
					break
			except :
				continue
	cv.destroyAllWindows()