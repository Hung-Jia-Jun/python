import requests
import pdb
from lxml import etree
import multiprocessing
import time 
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
    except:
        pass
ProcessData=[]
for Link in str(html).split('\\r\\n'):
    i+=1
    TargetUrl=Link.replace("b'","").replace("\\n'",'')
    print (i,TargetUrl)
    Filename=str(i)
    SaveFile(TargetUrl,str(FileItem)+Filename)
    time.sleep(0.1)
    #ProcessData.append([TargetUrl,Filename])
    #multiprocessing.Process(target=SaveFile,args=(TargetUrl,Filename,) ).start()
    
#multiprocessing.Process(target=SaveFile,args=(ProcessData[round(len(ProcessData)/2):]),) ).start()
#multiprocessing.Process(target=SaveFile,args=(ProcessData[:round(len(ProcessData)/2)]),) ).start()