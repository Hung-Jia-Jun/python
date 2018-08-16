import requests
import pdb
from lxml import etree
import multiprocessing
import time 
import cv2
import os
import tqdm
ListUrl=input('ListUrl:')
FileItem=input('Set FileName:')

#ListUrl="http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n12761284"
html = requests.get(str(ListUrl)).content
i=0
def SaveFile(TargetUrl,Filename):
    try:
        r = requests.get(TargetUrl)
        with open('Train/'+str(Filename)+'.jpg', 'wb') as f:  
            f.write(r.content)
        img = cv2.imread('Train/'+Filename+".jpg",0)
        try:
           Result=len(img)
        except:
           #print (Filename,"None")
           os.remove('Train/'+Filename+".jpg")
    except:
        pass

   

ProcessData=[]
for Link in tqdm.tqdm(str(html).split('\\r\\n')):
    i+=1
    TargetUrl=Link.replace("b'","").replace("\\n'",'')
    #print (i,TargetUrl)
    Filename=str(i)
    SaveFile(TargetUrl,str(FileItem)+Filename)
    time.sleep(0.1)
    #ProcessData.append([TargetUrl,Filename])
    #multiprocessing.Process(target=SaveFile,args=(TargetUrl,Filename,) ).start()
    
#multiprocessing.Process(target=SaveFile,args=(ProcessData[round(len(ProcessData)/2):]),) ).start()
#multiprocessing.Process(target=SaveFile,args=(ProcessData[:round(len(ProcessData)/2)]),) ).start()