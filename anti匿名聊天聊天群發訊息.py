# -*- coding: utf-8 -*-
import requests
import time,pdb,json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def StartRandomChat(sessionToken):
	headers = {
			#"X-Parse-Session-Token":"r:7a8445d79a2986668776faf1417e7413",
			"X-Parse-Session-Token":sessionToken,
			"X-Parse-Application-Id":"fUEmHsDqbr9v73s4JBx0CwANjDJjoMcDFlrGqgY5",
			"X-Parse-Installation-Id":"d9575738-8cd2-42ad-ac47-a7d782481f7e"
			#"X-Parse-Installation-Id":"7ec9ce9a-ea97-4904-ad9e-4a3b39081372"
			}
	payload={
	"platform": "ios",
	"v": "1518",
	"myLastChats": []
	}	
	RandomChatReq=requests.post("https://antich.at/parse/functions/startRandomChat", data=payload,verify=False,headers=headers).text
	try:
		ObjectID=RandomChatReq.split("objectId")[1].split(",")[0].replace('''":"''',"").split('"')[0]
		guestId=RandomChatReq.split("guestId")[1].split(",")[0].replace('''":"''',"").split('"')[0]
		return ObjectID,guestId
	except:
		return None,None

def SendRandomChatMsg(ObjectID,guestId,sessionToken): #發送隨機聊天的訊息
	global FuckMessages
	if (ObjectID==None or guestId==None):
		return None
	else:
		headers = {
			#"X-Parse-Session-Token":"r:7a8445d79a2986668776faf1417e7413",
			"X-Parse-Session-Token":sessionToken,
			"X-Parse-Application-Id":"fUEmHsDqbr9v73s4JBx0CwANjDJjoMcDFlrGqgY5",
			"X-Parse-Installation-Id":"d9575738-8cd2-42ad-ac47-a7d782481f7e"
			#"X-Parse-Installation-Id":"7ec9ce9a-ea97-4904-ad9e-4a3b39081372"
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
			print ("已發送邀請給"+str(guestId))
			#pdb.set_trace()
			file = open("已發送隨機聊天列表.txt","a") 
			file.write(str(guestId)+"\n") 
			file.close() 
IsSendList=[] #已發送訊息的列表


def Login(Username,Password):
	headers = {
			"X-Parse-Session-Token":"r:35f0141811f0babe645e20f3a19abe01",
			"X-Parse-Application-Id":"fUEmHsDqbr9v73s4JBx0CwANjDJjoMcDFlrGqgY5",
			"X-Parse-Installation-Id":"d9575738-8cd2-42ad-ac47-a7d782481f7e"
			#"X-Parse-Installation-Id":"7ec9ce9a-ea97-4904-ad9e-4a3b39081372"
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
	#req = requests.get('https://ps.pndsn.com/v2/subscribe/sub-c-24884386-3cf2-11e5-8d55-0619f8945a4f/9tM11YKWRN,DlpLqXVl4R,L8VRfrgFxI/0?deviceid=826FCAA8-9DBF-42C2-A01F-879F925F823F&uuid=9tM11YKWRN&pnsdk=PubNub-ObjC-iOS%2F4.6.1&auth=9tM11YKWRN1516626228&tt=15188086761225512',verify=False)
	#Reqtext=req.text
	ObjectID,guestId=StartRandomChat(sessionToken)
	SendRandomChatMsg(ObjectID,guestId,sessionToken)#建立隨機聊天並發送訊息

