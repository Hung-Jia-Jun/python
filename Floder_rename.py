# -*- coding: utf-8 -*-
import io,os,sys,shutil,pdb
from glob import glob

dirPath=""
dirNames=""
fileNames=""
def FloderContent():
    global dirPath,dirNames,fileNames
    SendMsg_Loca="C:/VCF_Contant"
    for dirPath, dirNames, fileNames in os.walk(SendMsg_Loca):  #use os.walk to add the same floder txt file
        dirPath=dirPath
        dirNames=dirNames
        fileNames=fileNames

FloderContent()

for file_Ele in fileNames:
    renamepath=str(dirPath)+"/"+str(file_Ele)
    file_Ele=file_Ele.replace(".txt","")
    New_rename=dirPath+"/"+file_Ele+"/"+file_Ele+".vcf"
    os.makedirs(dirPath+"/"+file_Ele)
    os.rename(renamepath,New_rename)
    #pdb.set_trace()
