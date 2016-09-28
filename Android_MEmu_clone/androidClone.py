# -*- coding: utf-8 -*-
import Floder_rename,android_adb
import os,pdb,re,time,io
from tqdm import tqdm
vmlist=[]
file_array=[]
re_dir_down=[]
TempFloderLen=0
FloderLen=0
dirNames=""
dirPath=""
fileNames=""

MEmuConsoleLoca=Floder_rename.Txt_io(2)
MEmuManageLoca=Floder_rename.Txt_io(3)
def Vm_mechine_list():
	global vmlist
	del vmlist[:] #clear the vms list contant
	regular_str="MEmu"
	commed=MEmuManageLoca+' list vms'
	#E:/android_Virtual/MEmuHyperv/MEmuManage.exe list vms
	osout=os.popen(commed).read()
	VM_len=len(re.findall(regular_str,osout))
	#pdb.set_trace()
	for i in range(1,VM_len+1):
		MEmu_name="MEmu"+osout.split("MEmu")[i]
		MEmu_name=MEmu_name.split('''"''')[0]
		vmlist.append(MEmu_name)
def FloderContent():
	global FloderLen,dirNames,dirPath,fileNames
	SendMsg_Loca=Floder_rename.Txt_io(1)
	for dirPath, dirNames, fileNames in os.walk(SendMsg_Loca):  #use os.walk to add the same floder txt file
		dirPath=dirPath
		dirNames=dirNames
		fileNames=fileNames
		FloderLen=len(dirNames)
		return FloderLen
		break

def modifyVM(hostpath):
	modifyVM_len=len(vmlist) #get vm list lenght
	for i in range(modifyVM_len): #get floder lenght
		try:
			Dirname_Ar_Regular='''"'''+vmlist[i]+'''"''' #regular the dirname add => " <=this word
			removeDir_cmd=MEmuManageLoca+" sharedfolder remove "+Dirname_Ar_Regular+" --name download"
			os.popen(removeDir_cmd) #remove the normal download dir
			addDir_cmd=MEmuManageLoca+" sharedfolder add "+Dirname_Ar_Regular+" --name download --hostpath "+hostpath[i]
			os.popen(addDir_cmd)
		except:
			vmlist.pop()
			pass

def CreateVm():
	global vmlist,nameArr
	TempvmLi=0
	FloderContent()
	Vm_mechine_list()
	nameArr=Floder_rename.RenameObj()
	bulid_want=len(nameArr)-len(vmlist)
	if bulid_want<0:
		pass
	else:
		print "bulid want",bulid_want
		while True: #get floder lenght to bulid vmware
			for i in tqdm(range(bulid_want)):
				commed=MEmuConsoleLoca+' clone MEmu'
				os.system(commed)
				time.sleep(25)
				commed_1=MEmuManageLoca+' sharedfolder remove "MEmu" --name download'
				os.system(commed_1) #remove the normal download dir
				commed_2=MEmuManageLoca+' sharedfolder add "MEmu" --name download --hostpath E:/android_Virtual/SDCard'
				os.system(commed_2)
			break

Floder_rename.Txt_io(0)
commed_3=MEmuManageLoca+' modifyvm MEmu_1 --name MEmu'
os.popen(commed_3)
CreateVm()
Vm_mechine_list()
print "Create meachine susessful!!!"
modifyVM(nameArr)
android_adb.adb_shell(vmlist)






