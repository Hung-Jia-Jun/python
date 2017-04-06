# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2,pdb

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



cap = cv2.VideoCapture(0)


cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)


while True:
	ret, image = cap.read()
	orig = image.copy()
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
	cv2.imshow("After NMS", image)

	cv2.waitKey(2)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break



cap.release()
cv2.destroyAllWindows()
