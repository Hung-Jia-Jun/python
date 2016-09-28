# -*- coding: utf-8 -*-
import io,os,sys,shutil,pdb
from glob import glob

dirPath=""
dirNames=""
fileNames=""
SendMsg_Loca=""



nameArr=[]
read_contant=[]
def Txt_io(line_num):
    del read_contant[:] #del the read file contant
    local=os.getcwd()
    io_open_cmd=local+"\Setting.inf"
    io_obj=io.open(io_open_cmd, 'r',encoding = 'utf-8') #文字檔位置
    while True:
        read_cont = io_obj.readline() #逐行讀取文字檔
        read_cont=read_cont.replace("\n","")
        read_contant.append(read_cont)
        if read_cont=="":
            break
    return read_contant[line_num]

def FloderContent(SendMsg_Loca):
    global dirPath,dirNames,fileNames
    #print u"電話簿資料夾: ",SendMsg_Loca
    for dirPath, dirNames, fileNames in os.walk(SendMsg_Loca):  #use os.walk to add the same floder txt file
        dirPath=dirPath
        dirNames=dirNames
        fileNames=fileNames

        nameArr.append(dirPath)

def RenameObj():
    SendMsg_Loca=Txt_io(0)
    FloderContent(SendMsg_Loca)
    #pdb.set_trace()
    for file_Ele in fileNames:
        renamepath=str(dirPath)+"/"+str(file_Ele) #get need rename path info
        file_Ele=file_Ele.replace(".txt","") #replace the .txt file name to " " none
        New_rename=dirPath+"/"+file_Ele+"/"+file_Ele+".vcf" #newrename is want to create to new location for use
        try:
            newmakeDir=dirPath+"/"+file_Ele #rename path floder name
            os.makedirs(newmakeDir) #do rename floder command
            os.rename(renamepath,New_rename) #move the renamed command suscessful file
            nameArr.append(newmakeDir) #add nameArr to return other application for get sharefloder location
        except:
            pass
    return nameArr #return nameArr to application get this name use to point sharefloder

#RenameObj()
