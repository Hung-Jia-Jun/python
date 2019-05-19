# -*- coding: UTF-8 -*-
from flask import Flask
import multiprocessing
import cv2
import ftplib
import os
import multiprocessing
import time
import ConfigParser
import pdb
import os
app = Flask(__name__)

#args=(DoPic,)
class Camera:
    def __init__(self):
        #self.DoPic = DoPic
        pass
    def Open(self,q):
        global frame
        cap = cv2.VideoCapture(0)
        cap.set(3,1920)
        cap.set(4,1080)
        while(True):
            # 從攝影機擷取一張影像
            ret, frame = cap.read()
            
            # 顯示圖片
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('c') or q.qsize() > 0:
                FileName=time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))+'.png'
                cv2.imwrite(FileName,frame,[cv2.IMWRITE_PNG_COMPRESSION, 0])
                multiprocessing.Process(target=upload,args=(FileName,) ).start()
                q.get()

            #break

        # 釋放攝影機
        cap.release()

        # 關閉所有 OpenCV 視窗
        cv2.destroyAllWindows()
    def SaveImage(self,q):
        q.put('1')

def ReadConfigFile():
    config = ConfigParser.ConfigParser()
    config.read('/home/pi/Desktop/Config.ini')
    FTP = config.get('Setting','FTP')
    FTPUsername = config.get('Setting','FTPUsername')
    FTPPassword = config.get('Setting','FTPPassword')
    return FTP,FTPUsername,FTPPassword
def upload(file):
    #Get Ftp username and password
    FTP,FTPUsername,FTPPassword = ReadConfigFile()
    
    ftp = ftplib.FTP(FTP)
    ftp.login(FTPUsername, FTPPassword)
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
    os.remove(file)
    
    


    print (file +" uploaded")

Camera = Camera()
q = multiprocessing.Queue()

multiprocessing.Process(target=Camera.Open,args=(q,)).start()

@app.route("/Pic")
def Pic():
    multiprocessing.Process(target=Camera.SaveImage,args=(q,)).start()
    return "OK"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
