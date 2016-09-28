# -*- coding: utf-8 -*-
import os,Floder_rename,sys,pdb
from time import *

ADB_vm_list=[]
MEmuConsoleloca=""
def  adb_shell(vm_list):
	global ADB_vm_list,MEmuConsoleloca
	ADB_vm_list=vm_list
	MEmuConsoleloca=Floder_rename.Txt_io(2)

	for i in range(1,len(ADB_vm_list)):
		MEmuConsole=MEmuConsoleloca+" "+ADB_vm_list[i]
		os.system(MEmuConsole) #start the vms
		print "Start Vm : ",ADB_vm_list[i]
	for ADB_List in range(1,len(ADB_vm_list)):
		if ADB_List==1:
			sleep(30) #waiting the vms boot
		vm_lenght=str(21503+(ADB_List*10))
		#pdb.set_trace()
		#system=popen
		os.system("taskkill /im adb.exe /f")
		os.system("adb connect 127.0.0.1:"+vm_lenght)  #connect the drives
		sleep(10)
		os.system("adb shell input tap 172 300") #tap the screan
		sleep(5)
		os.system("adb shell input keyevent 82") #tap the screan
		sleep(5)
		os.system("adb shell input tap 243 613") #tap the screan
		sleep(5)
		os.system("adb shell input tap 167 426") #tap the screan





