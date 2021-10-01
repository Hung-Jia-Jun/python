# -*- coding: utf-8 -*-
import requests
import time,pdb,json
import multiprocessing,pdb,sys,os,threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def StartRandomChat(sessionToken):
	headers = {
			#"X-Parse-Session-Token":"r:0000000000000000000000000000000000",
			"X-Parse-Session-Token":sessionToken,
			"X-Parse-Application-Id":"0000000000000000000000000000000000",
			"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			#"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			}
	payload={
	"platform": "ios",
	"v": "1518",
	"myLastChats": []
	}	
	try:
		RandomChatReq=requests.post("https://antich.at/parse/functions/startRandomChat", data=payload,verify=False,headers=headers).text
		ObjectID=RandomChatReq.split("objectId")[1].split(",")[0].replace('''":"''',"").split('"')[0]
		guestId=RandomChatReq.split("guestId")[1].split(",")[0].replace('''":"''',"").split('"')[0]
		guestname=RandomChatReq.split("guestname")[1].split(",")[0].replace('''":"''',"").split('"')[0]
		return ObjectID,guestId,guestname.split(" ")[0]
	except:
		return None,None,None
num=1
def SendRandomChatMsg(sessionToken): #發送隨機聊天的訊息
	global FuckMessages,num
	ObjectID,guestId,guestname=StartRandomChat(sessionToken)
	if (ObjectID==None or guestId==None):
		return None
	else:
		headers = {
			#"X-Parse-Session-Token":"0000000000000000000000000000000000",
			"X-Parse-Session-Token":sessionToken,
			"X-Parse-Application-Id":"0000000000000000000000000000000000",
			"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			#"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			}
		payload = {
		"dialogue": ObjectID,
		"message": FuckMessages,
		"receiver":guestId
		}
		file = open("已發送隨機聊天列表.txt", "r") 
		IsSendRandomList=file.read().split("\n")
		if guestId not in IsSendRandomList:
			SendStat=requests.post("https://antich.at/parse/classes/Messages", data=payload,verify=False,headers=headers).text
			try:
				print (str(num)+".已發送訊息給"+guestname+" ID:"+str(guestId))
			except:
				print (str(num)+".已發送訊息給"+str(guestId))
			num+=1
			#pdb.set_trace()
			file = open("已發送隨機聊天列表.txt","a") 
			file.write(str(guestId)+"\n") 
			file.close() 
IsSendList=[] #已發送訊息的列表


def Login(Username,Password):
	headers = {
			"X-Parse-Session-Token":"0000000000000000000000000000000000",
			"X-Parse-Application-Id":"0000000000000000000000000000000000",
			"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			#"X-Parse-Installation-Id":"0000000000000000000000000000000000"
			}
	payload={
	"_method": "GET",
	"username": Username,
	"password": Password
	}
	LoginReq=requests.post("https://antich.at/parse/login", data=payload,verify=False,headers=headers).text
	return json.loads(LoginReq)["sessionToken"]


Username=input("請輸入帳號:")
Password=input("請輸入密碼:")
FuckMessages=input("請輸入要發的訊息:")
sessionToken=Login(Username,Password)
while True:
	#Reqtext=req.text
	#threading.Thread(target=SendRandomChatMsg,args=(sessionToken,)).start() #建立隨機聊天並發送訊息
	SendRandomChatMsg(sessionToken)

