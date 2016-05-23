# -*- coding: utf-8 -*-
import unittest, time, re,sys
import datetime, time
import io
import os
for loop in range(10, 0, -1):
	f=io.open('D:\unity\Unity_5.1_Project\ChineseRecognize_5.3-2\Speech recognition5.3\Assets\A.txt', 'r',encoding = 'UTF-8')
	#print (content)
	if "false" in f:
		print u"已接收到unity 錯誤指令"
	else:
		os.system("pause")
		