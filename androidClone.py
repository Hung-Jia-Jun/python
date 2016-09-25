# -*- coding: utf-8 -*-

import os,pdb
os.system('E:/android_Virtual/MEmuHyperv/MEmuManage.exe import C:/Users/Jason/Desktop/備份用.ova')
os.system('E:/android_Virtual/MEmuHyperv/MEmuManage.exe sharedfolder remove "MEmu_1" --name download') #remove the normal download dir
os.system('E:/android_Virtual/MEmuHyperv/MEmuManage.exe sharedfolder add "MEmu_1" --name download --hostpath E:/android_Virtual/SDCard')
file_array=[]
re_dir_down=[]
TempFloderLen=0
FloderLen=0
dirNames=""
def FloderContent():
	global FloderLen,dirNames
	SendMsg_Loca="E:/android_Virtual/MEmu/MemuHyperv VMs"
	for dirPath, dirNames, fileNames in os.walk(SendMsg_Loca):  #use os.walk to add the same floder txt file
		#print dirNames
		FloderLen=len(dirNames)
		return FloderLen
		break

def modifyVM():
	FloderLen=FloderContent()
	for i in range(FloderLen): #get floder lenght
		print i
		Dirname_Ar_Regular='''"'''+dirNames[i-1]+'''"''' #regular the dirname add => " <=this word
		removeDir_cmd="E:/android_Virtual/MEmuHyperv/MEmuManage.exe sharedfolder remove "+Dirname_Ar_Regular+" --name download"
		os.system(removeDir_cmd) #remove the normal download dir
		addDir_cmd="E:/android_Virtual/MEmuHyperv/MEmuManage.exe sharedfolder add "+Dirname_Ar_Regular+" --name download --hostpath E:/android_Virtual/SDCard"
		os.system(addDir_cmd)
		print "Remove:   ",removeDir_cmd
		print "add:   ",addDir_cmd
		print "Dir name :",Dirname_Ar_Regular
		print "susessful!!",Dirname_Ar_Regular

FloderContent()
normal_len=FloderLen #normal floder len is application running befor len


needAdd=2  #user need to add vmware to meachine can change this variable


target_len=normal_len+needAdd #target_len is loop break codition
#modifyVM()


"""
while True:
	FloderLen=FloderContent()
	if TempFloderLen != FloderLen:
		FloderContent()
		os.system('E:/android_Virtual/MEmuHyperv/MEmuManage.exe import C:/Users/Jason/Desktop/備份用.ova')
		print "Create"
		print "Temp",TempFloderLen
		print "floder len:",FloderLen
		print "Normal: ",normal_len
		print "Target: ",target_len
		TempFloderLen=len(dirNames)
	if FloderLen==target_len:
		break
"""

