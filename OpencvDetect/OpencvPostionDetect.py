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

ilowH = 0
ihighH = 179

ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255
#cv2.createTrackbar('lowH','image',ilowH,179,do_nothing)
#cv2.createTrackbar('highH','image',ihighH,179,do_nothing)

#cv2.createTrackbar('lowS','image',ilowS,255,do_nothing)
#cv2.createTrackbar('highS','image',ihighS,255,do_nothing)

#cv2.createTrackbar('lowV','image',ilowV,255,do_nothing)
#cv2.createTrackbar('highV','image',ihighV,255,do_nothing)
#cv2.namedWindow('image') #開啟設定窗口

def PointTakeing(frame):#分離三點
    HSVColor  =  cv2.cvtColor (frame,cv2.COLOR_BGR2HSV)#轉換RGB變成HSV圖像
    #----A點
    # get trackbar positions
    ilowH = 0#cv2.getTrackbarPos('lowH', 'image')
    ihighH =0#cv2.getTrackbarPos('highH', 'image')
    ilowS = 0#cv2.getTrackbarPos('lowS', 'image')
    ihighS =11#cv2.getTrackbarPos('highS', 'image')
    ilowV = 255#cv2.getTrackbarPos('lowV', 'image')
    ihighV =255#cv2.getTrackbarPos('highV', 'image')

    HSVlower = np.array([ilowH,ilowS,ilowV])#低彩度設置[h,s,v]
    HSVupper = np.array([ihighH,ihighS,ihighV])#高彩度設置[h,s,v]
    mask = cv2.inRange(HSVColor, HSVlower, HSVupper)#取出特徵值
    #cv2.imshow('image', mask) 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 10))

    #侵蝕
    eroded = cv2.erode(mask,kernel)
    #膨脹圖像
    dilated = cv2.dilate(eroded,kernel)
    #顯示膨脹後的圖像
    cv2.imshow("Dilated Image",dilated);
    


    ret,threshA=cv2.threshold(dilated,0,255,cv2.THRESH_BINARY_INV)#二值化影像
    image,contours,hierarchy = cv2.findContours(threshA,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  
    cnt=[]
    font_1_X=""
    font_1_Y=""
    if len(contours) > 0:
        cnt=contours[0]
        print (np.amax(cnt)-np.amin(cnt))
        cv2.drawContours(frame,cnt,0,(0,0,255),100) #繪製點在球上
        font_1_X=cnt[0,0,0]#從座標陣列cnt提取出X來給顯示點1上的數字座標
        font_1_Y=cnt[0,0,1]#從座標陣列cnt提取出Y來給顯示點1上的數字座標
        str_Point_1='  ('+str(font_1_X)+','+str(font_1_Y)+')'
        cv2.putText(frame, str_Point_1 ,(font_1_X,font_1_Y), 0 , 0.5 , ( 0 , 0 , 255 ), 1 )
        #print (str_Point_1)

    else:
        print ("Sorry No contour Found.")

    return font_1_X,font_1_Y
    #----C點
    pass
def run_thread(): #A相機
    cap = cv2.VideoCapture(0)

    while True:
        ret0, frame = cap.read()#讀取攝影機的物件
        TakeingResaul= PointTakeing(frame)#依序推入需要計算的XY值，並且依照位置獲取指定的字元
        cv2.imshow('X', frame) 
        cv2.waitKey(5)
        pass

    pass
    
if __name__ == '__main__':   
    run_thread()
    #p1 = multiprocessing.Process(target=run_thread )
    #p4 = multiprocessing.Process(target=detailTxt)


    #pdb.set_trace()
    #p1.start()
    #p2.start()
    #raw_input()
    #p1.start()
    
    #detailTxt()