# -*- coding: utf-8 -*-
from urllib.parse import quote
from urllib.parse import unquote
from bson.objectid import ObjectId
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time,sys
from bs4 import BeautifulSoup
import io,pdb,random
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import socket
import _thread
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
import sqlite3
import base64
from pymongo import MongoClient
import json
import time
import string
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
## 输出时间
#def job():
##    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
## BlockingScheduler
#scheduler = BlockingScheduler()
#scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
#scheduler.start()

#各功能的開通資料表
Feature={
  "FB自動幫好友按讚": "AutoLike",
  "FB自動幫好友留言": "AutoComment",
  "FB自動偵測幽靈人": "FB_DetectGhost",
  "FB個人發文被按讚": "FB_PostGetLike_Person",
  "FB個人發文被留言": "FB_PostGetComment_Person",
  "FB個人分享被按讚": "FB_ShareGetLike_Person",
  "FB個人打卡被按讚": "FB_LandMarksLike_Person",
  "IG個人發文被按讚": "IG_PostGetLike_Person",
  "FB個人被標被按讚": "FB_MarkGetLike_Person",
  "FB個人帳戶被追蹤": "FB_GetTrack_Person",
  "FB個人貼文被分享": "FB_PostGetShare_Person",
  "FB粉專發文被按讚": "FB_PostGetLike_FanPage",
  "FB粉專發文被留言": "FB_PostGetComment_FanPage",
  "FB粉專帳戶被追蹤": "FB_GetTrack_FanPage",
  "FB粉專貼文被分享": "FB_PostGetShare_FanPage",
  "FB社團發文被按讚": "FB_PostGetLike_Community",
  "FB社團發文被留言": "FB_PostGetComment_Community",
  "FB社團帳戶被追蹤": "FB_GetTrack_Community",
  "FB社團貼文被分享": "FB_PostGetShare_Community",
  "IG自動幫好友按讚": "IG_AutoLike",
  "IG自動幫好友留言": "IG_AutoComment",
  "IG自動偵測幽靈人": "IG_DetectGhost",
  "IG個人發文被留言": "IG_PostGetComment_Person",
  "IG個人帳戶被追蹤": "IG_GetTrack_Person",
  "IG商業發文被按讚": "IG_PostGetLike_Business",
  "IG商業發文被留言": "IG_PostGetComment_Business",
  "IG商業帳戶被追蹤": "IG_GetTrack_Business"
}


#被做動的功能資料表
BuyOther_Feature={
  "FB個人發文被按讚": "TaskDoType|Like|TaskURLtype|Self|",#               任務類型     讚(Like)        任務目標URL類型    個人(Self)
  "FB個人發文被留言": "TaskDoType|Comments|TaskURLtype|Self|",#           任務類型     留言(Comments)  任務目標URL類型    個人(Self)
  "FB個人帳戶被追蹤": "TaskDoType|Follow|TaskURLtype|Self|",#             任務類型     追蹤(Follow)    任務目標URL類型    個人(Self)
  "FB個人貼文被分享": "TaskDoType|Share|TaskURLtype|Self|",#              任務類型     分享(Share)     任務目標URL類型    個人(Self)
  "FB粉專發文被按讚": "TaskDoType|Like|TaskURLtype|Fanpage|",#            任務類型     讚(Like)        任務目標URL類型    粉專(Fanpage)
  "FB粉專發文被留言": "TaskDoType|Comments|TaskURLtype|Fanpage|",#        任務類型     留言(Comments)  任務目標URL類型    粉專(Fanpage)
  "FB粉專帳戶被追蹤": "TaskDoType|Follow|TaskURLtype|Fanpage|",#          任務類型     追蹤(Follow)    任務目標URL類型    粉專(Fanpage)
  "FB粉專貼文被分享": "TaskDoType|Share|TaskURLtype|Fanpage|",#           任務類型     分享(Share)     任務目標URL類型    粉專(Fanpage)
  "FB社團發文被按讚": "TaskDoType|Like|TaskURLtype|Group|",#              任務類型     讚(Like)        任務目標URL類型    社團(Group)
  "FB社團發文被留言": "TaskDoType|Comments|TaskURLtype|Group|",#          任務類型     留言(Comments)  任務目標URL類型    社團(Group)
  "FB社團帳戶被追蹤": "TaskDoType|Follow|TaskURLtype|Group|",#            任務類型     追蹤(Follow)    任務目標URL類型    社團(Group)
  "FB社團貼文被分享": "TaskDoType|Share|TaskURLtype|Group|",#             任務類型     分享(Share)     任務目標URL類型    社團(Group)
}



FeatureTheKeys=["FB自動幫好友按讚","FB自動幫好友留言","FB自動偵測幽靈人","FB個人發文被按讚","FB個人發文被留言","FB個人分享被按讚","FB個人打卡被按讚","IG個人發文被按讚","FB個人被標被按讚","FB個人帳戶被追蹤","FB個人貼文被分享","FB粉專發文被按讚","FB粉專發文被留言","FB粉專帳戶被追蹤","FB粉專貼文被分享","FB社團發文被按讚","FB社團發文被留言","FB社團帳戶被追蹤","FB社團貼文被分享","IG自動幫好友按讚","IG自動幫好友留言","IG自動偵測幽靈人","IG個人發文被按讚","IG個人發文被留言","IG個人帳戶被追蹤","IG商業發文被按讚","IG商業發文被留言","IG商業帳戶被追蹤"]
def ChangeKeyENG_To_CHT(ConverText): #將英文的key變成中文的key
	ConverText=ConverText.replace("AutoLike","FB自動幫好友按讚")
	ConverText=ConverText.replace("AutoComment","FB自動幫好友留言")
	ConverText=ConverText.replace("AutoComment","FB自動幫好友留言")
	ConverText=ConverText.replace("FB_DetectGhost","FB自動偵測幽靈人")
	ConverText=ConverText.replace("FB_PostGetLike_Person","FB個人發文被按讚")
	ConverText=ConverText.replace("FB_PostGetComment_Person","FB個人發文被留言")
	ConverText=ConverText.replace("FB_ShareGetLike_Person","FB個人分享被按讚")
	ConverText=ConverText.replace("FB_LandMarksLike_Person","FB個人打卡被按讚")
	ConverText=ConverText.replace("IG_PostGetLike_Person","IG個人發文被按讚")
	ConverText=ConverText.replace("FB_MarkGetLike_Person","FB個人被標被按讚")
	ConverText=ConverText.replace("FB_GetTrack_Person","FB個人帳戶被追蹤")
	ConverText=ConverText.replace("FB_PostGetShare_Person","FB個人貼文被分享")
	ConverText=ConverText.replace("FB_PostGetLike_FanPage","FB粉專發文被按讚")
	ConverText=ConverText.replace("FB_PostGetComment_FanPage","FB粉專發文被留言")
	ConverText=ConverText.replace("FB_GetTrack_FanPage","FB粉專帳戶被追蹤")
	ConverText=ConverText.replace("FB_PostGetShare_FanPage","FB粉專貼文被分享")
	ConverText=ConverText.replace("FB_PostGetLike_Community","FB社團發文被按讚")
	ConverText=ConverText.replace("FB_PostGetComment_Community","FB社團發文被留言")
	ConverText=ConverText.replace("FB_GetTrack_Community","FB社團帳戶被追蹤")
	ConverText=ConverText.replace("FB_PostGetShare_Community","FB社團貼文被分享")
	ConverText=ConverText.replace("IG_AutoLike","IG自動幫好友按讚")
	ConverText=ConverText.replace("IG_AutoComment","IG自動幫好友留言")
	ConverText=ConverText.replace("IG_DetectGhost","IG自動偵測幽靈人")
	ConverText=ConverText.replace("IG_PostGetLike_Person","IG個人發文被按讚")
	ConverText=ConverText.replace("IG_PostGetComment_Person","IG個人發文被留言")
	ConverText=ConverText.replace("IG_GetTrack_Person","IG個人帳戶被追蹤")
	ConverText=ConverText.replace("IG_PostGetLike_Business","IG商業發文被按讚")
	ConverText=ConverText.replace("IG_PostGetComment_Business","IG商業發文被留言")
	ConverText=ConverText.replace("IG_GetTrack_Business","IG商業帳戶被追蹤")
	return ConverText
def ChangeKeyCHT_To_ENG(ConverText): #將英文的key變成英文的key
	ConverText=ConverText.replace("FB自動幫好友按讚","AutoLike")
	ConverText=ConverText.replace("FB自動幫好友留言","AutoComment")
	ConverText=ConverText.replace("FB自動幫好友留言","AutoComment")
	ConverText=ConverText.replace("FB自動偵測幽靈人","FB_DetectGhost")
	ConverText=ConverText.replace("FB個人發文被按讚","FB_PostGetLike_Person")
	ConverText=ConverText.replace("FB個人發文被留言","FB_PostGetComment_Person")
	ConverText=ConverText.replace("FB個人分享被按讚","FB_ShareGetLike_Person")
	ConverText=ConverText.replace("FB個人打卡被按讚","FB_LandMarksLike_Person")
	ConverText=ConverText.replace("IG個人發文被按讚","IG_PostGetLike_Person")
	ConverText=ConverText.replace("FB個人被標被按讚","FB_MarkGetLike_Person")
	ConverText=ConverText.replace("FB個人帳戶被追蹤","FB_GetTrack_Person")
	ConverText=ConverText.replace("FB個人貼文被分享","FB_PostGetShare_Person")
	ConverText=ConverText.replace("FB粉專發文被按讚","FB_PostGetLike_FanPage")
	ConverText=ConverText.replace("FB粉專發文被留言","FB_PostGetComment_FanPage")
	ConverText=ConverText.replace("FB粉專帳戶被追蹤","FB_GetTrack_FanPage")
	ConverText=ConverText.replace("FB粉專貼文被分享","FB_PostGetShare_FanPage")
	ConverText=ConverText.replace("FB社團發文被按讚","FB_PostGetLike_Community")
	ConverText=ConverText.replace("FB社團發文被留言","FB_PostGetComment_Community")
	ConverText=ConverText.replace("FB社團帳戶被追蹤","FB_GetTrack_Community")
	ConverText=ConverText.replace("FB社團貼文被分享","FB_PostGetShare_Community")
	ConverText=ConverText.replace("IG自動幫好友按讚","IG_AutoLike")
	ConverText=ConverText.replace("IG自動幫好友留言","IG_AutoComment")
	ConverText=ConverText.replace("IG自動偵測幽靈人","IG_DetectGhost")
	ConverText=ConverText.replace("IG個人發文被按讚","IG_PostGetLike_Person")
	ConverText=ConverText.replace("IG個人發文被留言","IG_PostGetComment_Person")
	ConverText=ConverText.replace("IG個人帳戶被追蹤","IG_GetTrack_Person")
	ConverText=ConverText.replace("IG商業發文被按讚","IG_PostGetLike_Business")
	ConverText=ConverText.replace("IG商業發文被留言","IG_PostGetComment_Business")
	ConverText=ConverText.replace("IG商業帳戶被追蹤","IG_GetTrack_Business")
	return ConverText
class MongoController: #mongodb 控制器
	def __init__(self): 
		self.client  = MongoClient('mongodb://UserName:Password@127.0.0.1:22453/')
		self.db      = self.client['FB_User']
		self.collect = self.db['UserCol']
		
	def GetCursor(self): #取得控制器
		return self.collect

	def OrderDB(self): #訂單管理資料庫

		self.client  = MongoClient('mongodb://UserName:Password@127.0.0.1:22453/')
		self.db      = self.client['FB_User']
		self.collect = self.db['OrderDB'] #訂單管理資料庫
		return self.collect
	def TaskDB(self):
		self.client  = MongoClient('mongodb://UserName:Password@127.0.0.1:22453/')
		self.db      = self.client['TaskDB']
		self.collect = self.db['FB_Task'] #FB 任務資料庫
		return self.collect
def AddUserStickers(request): #更新使用者大頭貼
	Username     = request.GET.get("Username", '') #使用者帳號
	UserStickers = request.GET.get("UserStickers", '') #使用者大頭貼的處理
	DBController = MongoController().GetCursor()#取得資料庫使用權
	DBController.update_one({ #更新用戶資料
	  "Username": Username
	},{
	  '$set': {
		"UserStickers": UserStickers #更新用戶大頭貼
	  }
	}, upsert=False)
	return HttpResponse("OK")

def GetAllComment(request): #取得所有預設，自訂的留言
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #使用者密碼
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController = MongoController().GetCursor()#取得資料庫使用權
		UserBuyInfo     = DBController.find_one({"98Username": Username},{'_id':False,"FB_ADUser":1,"IG_ADUser":1})#取得用戶目前購買狀態是廣告用戶還是一般用戶
		

		#Custom_FB_Comment_Arr        自訂FB用戶留言
		#Normal_FB_Comment_Arr        預設FB用戶留言
		#AD_Custom_FB_Comment_Arr     廣告用戶的自訂FB用戶留言   
		#AD_Normal_FB_Comment_Arr     廣告用戶的預設FB用戶留言   

		#Custom_IG_Comment_Arr        自訂IG用戶留言
		#Normal_IG_Comment_Arr        預設IG用戶留言
		#AD_Custom_IG_Comment_Arr     廣告用戶的自訂IG用戶留言      
		#AD_Normal_IG_Comment_Arr     廣告用戶的預設IG用戶留言      

		AllComments=DBController.find_one({"98Username": Username},{'_id':False,"Custom_FB_Comment_Arr":1,"Normal_FB_Comment_Arr":1,"AD_Custom_FB_Comment_Arr":1,"AD_Normal_FB_Comment_Arr":1,"Custom_IG_Comment_Arr":1,"Normal_IG_Comment_Arr":1,"AD_Custom_IG_Comment_Arr":1,"AD_Normal_IG_Comment_Arr":1})
		ReturnStr=""
	
		


		#FB
		if UserBuyInfo["FB_ADUser"]=="true": #廣告用戶
			ReturnStr+=AllComments["AD_Custom_FB_Comment_Arr"]+";"
			ReturnStr+=AllComments["AD_Normal_FB_Comment_Arr"]+";"
		else:
			ReturnStr+=AllComments["Custom_FB_Comment_Arr"]+";"
			ReturnStr+=AllComments["Normal_FB_Comment_Arr"]+";"

		#IG
		if UserBuyInfo["IG_ADUser"]=="true": #廣告用戶
			ReturnStr+=AllComments["AD_Custom_IG_Comment_Arr"]+";"
			ReturnStr+=AllComments["AD_Normal_IG_Comment_Arr"]+";"
		else:
			ReturnStr+=AllComments["Custom_IG_Comment_Arr"]+";"
			ReturnStr+=AllComments["Normal_IG_Comment_Arr"]+";"
			
		return HttpResponse(str(ReturnStr))
	else:
		return HttpResponse("LoginFail")



def GetUserStickers(request): #取得使用者大頭貼
	Username     = request.GET.get("Username", '') #使用者帳號
	DBController = MongoController().GetCursor()#取得資料庫使用權
	UserInfo     = DBController.find_one({"98Username": Username},{'_id':False,"UserStickers":1})["UserStickers"]#取得使用者大頭貼
	return HttpResponse(UserInfo)
def ToggleCustomComments(request): #切換留言使用群組
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #使用者密碼
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController.update_one({ #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"Comments": Comments #填入用戶留言
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")


def GetGhostList(request): #取得幽靈列表
	Username     = request.GET.get("Username", '') #使用者帳號
	Password     = request.GET.get("Password", '') #使用者密碼
	ItemPos      = request.GET.get("ItemPos", '') #取得第幾位幽靈
	DBController = MongoController().GetCursor()#取得資料庫使用權
	GhostList    = DBController.find_one({"98Username": Username},{'_id':False})["GhostList"].split("|")[int(ItemPos)]#取得第幾位幽靈
	return HttpResponse(GhostList)


def GetGhostListTotal(request): #取得幽靈列表總數
	Username     = request.GET.get("Username", '') #使用者帳號
	Password     = request.GET.get("Password", '') #使用者密碼
	DBController = MongoController().GetCursor()#取得資料庫使用權
	GhostList    = DBController.find_one({"98Username": Username},{'_id':False})["GhostList"]#取得使用者大頭貼
	Last_GhostCheckTime    = DBController.find_one({"98Username": Username},{'_id':False})["Last_GhostCheckTime"]#取得使用者最後一次更新幽靈列表的時間
	format="%Y/%m/%d-%H:%M:%S"
	if (Last_GhostCheckTime==""):
		return HttpResponse(str(len(GhostList.split("|")))+"|"+"")
	else:
		return HttpResponse(str(len(GhostList.split("|")))+"|"+str(int((datetime.datetime.now()-datetime.datetime.strptime(Last_GhostCheckTime, format)).seconds/60)))

def AddRecommendedPerson(request):#新增推薦人
	Username          = request.GET.get("Username", '') #使用者帳號
	RecommendedPerson = request.GET.get("RecommendedPerson", '')
	DBController      = MongoController().GetCursor()#取得資料庫使用權
	try:
		if DBController.find_one({"98Username": Username},{'_id':False})["RecommendedPerson"]!=None:
			if DBController.find_one({"98Username": Username},{'_id':False})["RecommendedPerson"]=="None":
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"RecommendedPerson": RecommendedPerson #填入推薦人名稱
				  }
				}, upsert=False)
			else:
				return HttpResponse("Exist")
			UserInfo=str(DBController.find_one({"98Username": Username},{'_id':False}))#取得使用者基本資料
			UserInfo=json.dumps(UserInfo)#轉成json格式
			return HttpResponse(UserInfo)#將使用者資料回傳回客戶端
		else:
			return HttpResponse("Error")
	except:
		return HttpResponse("Error")
def GetRecommendedPerson(request):#下載推薦人
	Username          = request.GET.get("Username", '') #使用者帳號
	DBController      = MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"98Username": Username},{'_id':False})["RecommendedPerson"]!=None:
		RecommendPerson=DBController.find_one({"98Username": Username},{'_id':False})["RecommendedPerson"]
		if RecommendPerson=="":
			return HttpResponse("-----")
		else:
			return HttpResponse(DBController.find_one({"98Username": Username},{'_id':False})["RecommendedPerson"])#將使用者資料回傳回客戶端
	else:
		return HttpResponse("-----")
def AddLikeCount(request): #增加一次按讚次數
	Username     = request.GET.get("Username", '') #使用者帳號
	DBController = MongoController().GetCursor()#取得資料庫使用權
	MultiAddLike = request.GET.get("MultiAddLike", '') #一次新增多筆讚
	UserInfo     = DBController.find_one({"Username": Username},{'_id':False})#取得使用者基本資料
	DBController.update_one({ #更新用戶資料
	  "Username": Username
	},{
	  '$set': {
	  	"Latest_Like_Update":str(time.strftime("%Y/%m/%d-%H:%M:%S")),#將這次按讚的時間
		"LikeCount": UserInfo["LikeCount"]+int(MultiAddLike), #填入幽靈列表
		"IsSleep":"false", #休息完畢了
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端

def AddCommentCount(request): #增加一次留言次數
	Username   =request.GET.get("Username", '') #使用者帳號
	DBController=MongoController().GetCursor()#取得資料庫使用權
	MultiAddComment = request.GET.get("MultiAddComment", '') #一次新增多筆留言計數器
	UserInfo=DBController.find_one({"Username": Username},{'_id':False})#取得使用者基本資料
	DBController.update_one({ #更新用戶資料
	  "Username": Username
	},{
	  '$set': {
		"CommentCount": UserInfo["CommentCount"]+int(MultiAddComment), #新增留言數
		"IsSleep":"false", #休息完畢了
	  }
	}, upsert=False)
	
	UserInfo=str(DBController.find_one({"Username": Username},{'_id':False}))#取得使用者基本資料
	UserInfo=json.dumps(UserInfo)#轉成json格式
	return HttpResponse(UserInfo)#將使用者資料回傳回客戶端
def UploadGhostList(request): #使用者上傳幽靈列表
	Username   = request.GET.get("Username", '') #使用者帳號
	GhostLi    = request.GET.get("GhostLi", '')
	DBController=MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"Username": Username},{"GhostList":1})["GhostList"]=="none":
		DBController.update_one({"Username": Username},{'$set': {"GhostCheck":False,"GhostList": ""}}, upsert=False)

	DBController.update_one({ #更新用戶資料
	  "Username": Username
	},{
	  '$set': {
		"GhostCheck":False,#查詢幽靈的開關關閉
		"GhostList": DBController.find_one({"Username": Username},{"GhostList":1})["GhostList"]+"|"+GhostLi #填入幽靈列表
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端

	
def UploadGhostSussful(request): #清空用戶的幽靈列表
	Username     = request.GET.get("Username", '') #使用者帳號
	Password     = request.GET.get("Password", '') #使用者密碼
	DBController = MongoController().GetCursor()#取得資料庫使用權
	DBController.update_one({ #更新用戶資料
	  "Username": Username,
	  "Password": Password
	},{
	  '$set': {
	  	"GhostList": "none", #清空幽靈列表
		"DelUrl": "" #清空要刪除的幽靈列表
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端
def UploadWantDelList(request): #使用者上傳要刪除的幽靈列表，進行刪除的動作
	Username     = request.GET.get("Username", '') #使用者帳號
	DelUrl       = request.GET.get("DelUrl", '') #刪除列表
	DBController = MongoController().GetCursor()#取得資料庫使用權
	if DelUrl=="Clear": #清空幽靈列表
		DBController.update_one({ #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"GhostList": "none", #清空幽靈列表
			"GhostCheck": True, #使用者開始偵測幽靈狀態
			"Last_GhostCheckTime":str(time.strftime("%Y/%m/%d-%H:%M:%S")),#最後一次啟動搜尋幽靈的時間
		  }
		}, upsert=False)
		return HttpResponse("OK")#將使用者資料回傳回客戶端
	if DelUrl    == "OK": #結束運行刪除幽靈了
		DBController.update_one({ #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"DelUrl": "" #填入要刪除的幽靈列表
		  }
		}, upsert=False)
	else: #接收上傳的幽靈列表
		DBController.update_one({ #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"DelUrl": DelUrl #填入要刪除的幽靈列表
		  }
		}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端
def CreateAccount(request):
	Userinfo     = request.GET.get("Userinfo", '') #使用者帳號

	CreateInfo=Userinfo.split("|")
	while '' in CreateInfo:CreateInfo.remove('')

	if CreateInfo[8]=="None":#FB帳號
		CreateInfo[8]=""
	if CreateInfo[9]=="None":#FB密碼
		CreateInfo[9]=""
	if CreateInfo[10]=="None":#IG帳號
		CreateInfo[10]=""
	if CreateInfo[11]=="None":#IG密碼
		CreateInfo[11]=""
	DBController= MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"98Username":  CreateInfo[6]})!=None: #如果找不到這個98使用者，可以創建98用戶
		#98用戶已註冊過
		return HttpResponse("98User is exist")


		if DBController.find_one({"Username": CreateInfo[8]})!=None: #確認這個FB帳號沒被註冊過
			#FB用戶已註冊過
			return HttpResponse("FB User is exist")

	try:
		DBController.insert_one(
			{"98Username":                 CreateInfo[6], #98帳號
			"98Password":                  CreateInfo[7], #98密碼
			"Username":                    CreateInfo[8], #FB帳號 
			"Password":                    CreateInfo[9], #FB密碼 
			"IG_Username":                 CreateInfo[10], #IG帳號
			"IG_Password":                 CreateInfo[11], #IG密碼
			"Email":                       CreateInfo[12],#Email
			"CanLogin":                    True, #預設都可以被登入
			"UserStatus":                  False, #使用者登入狀態
			"LatestUpdate":                str(time.strftime("%Y/%m/%d-%H:%M:%S")),
			"PhoneLoginLog":               str(time.strftime("%Y/%m/%d-%H:%M:%S")), #手機登入時間
			"PCLoginLog":                  "",#PC端登入紀錄  IP位置/時間/登入狀態
			"SelfPage":                    "",
			"IsSleep": "",#此帳號正在休息時間，暫停按讚
			"AutoLike":                    False,
			"AutoComment":                 False,
			"GhostList":                   "none",
			"GhostCheck":                  False,
			"DelGhost":                    False,
			"LikeCount":                   0.0,
			"CommentCount":                0.0,
			"RecommendedPerson":           "None",
			"DelUrl":                      "",
			"FB_DetectGhost":              False,
			"FB_PostGetLike_Person":       False,
			"FB_PostGetComment_Person":    False,
			"FB_ShareGetLike_Person":      False,
			"FB_LandMarksLike_Person":     False,
			"IG_PostGetLike_Person":       False,
			"FB_MarkGetLike_Person":       False,
			"FB_GetTrack_Person":          False,
			"FB_PostGetShare_Person":      False,
			"FB_PostGetLike_FanPage":      False,
			"FB_PostGetComment_FanPage":   False,
			"FB_GetTrack_FanPage":         False,
			"FB_PostGetShare_FanPage":     False,
			"FB_PostGetLike_Community":    False,
			"FB_PostGetComment_Community": False,
			"FB_GetTrack_Community":       False,
			"FB_PostGetShare_Community":   False,
			"IG_AutoLike":                 False,
			"IG_AutoComment":              False,
			"IG_DetectGhost":              False,
			"Latest_Like_Update":          "",
			"IG_PostGetComment_Person":    False,
			"IG_GetTrack_Person":          False,
			"IG_PostGetLike_Business":     False,
			"IG_PostGetComment_Business":  False,
			"IG_GetTrack_Business":        False,
			"FeaturesLi":                  "",
			"FB_Comment_Arr":              "",
			"IG_Comment_Arr":              "",
			"UUID":                        "", #加入空的UUID
			"FanpageURL":                  "",
			"UserStickers":                "",
			"RealName":                    CreateInfo[0],#真實姓名
			"Address":                     CreateInfo[1],#地址
			"Phone":                       CreateInfo[2],#電話
			"IDCardNumber":                CreateInfo[3],#身份證字號
			"sex":                         CreateInfo[4],#性別
			"Birthday":                    CreateInfo[5],#生日
			"FB_Last_StartTime":           "",#這次啟動紀錄當前系統時間作為起始時間
			"FBstartClick":                False,#FB是否要開始按讚了
			"GroupURL":                    "",
			"ServiceAccount":              False, #除非另外設定，不然都不會是客服帳戶
			"Custom_FB_Comment_Arr":       "false%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%7Cfalse%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%7Cfalse%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%7Cfalse%2Chi%2Chi%7Cfalse%2CHi%2CHi%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%7C%0D%0A",
			"Normal_FB_Comment_Arr":       "false%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%7Cfalse%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%7Cfalse%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%7Cfalse%2Chi%2Chi%7Cfalse%2CHi%2CHi%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%7C%0D%0A",
			"AD_Normal_IG_Comment_Arr":    "true%2C98%20Social%20APP%E5%BB%A3%E5%91%8A%E6%96%87%2C%E4%BD%A0%E4%B9%9F%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%EF%BC%9F%20%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C%E5%8E%9F%E4%BE%86%E5%A4%A7%E5%AE%B6%E9%83%BD%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%20%E5%95%8A%EF%BC%81%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%20Social%20APP%20%E7%9C%9F%E7%9A%84%E5%A4%AA%E5%A5%BD%E7%94%A8%E4%BA%86%EF%BC%8C%E5%A4%A7%E6%8E%A8%2B1%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Cfalse%2Chi%2Chi%7Cfalse%2CHi%2CHi%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%7C",
			"AD_Normal_FB_Comment_Arr":    "true%2C98%20Social%20APP%E5%BB%A3%E5%91%8A%E6%96%87%2C%E4%BD%A0%E4%B9%9F%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%EF%BC%9F%20%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C%E5%8E%9F%E4%BE%86%E5%A4%A7%E5%AE%B6%E9%83%BD%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%20%E5%95%8A%EF%BC%81%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%20Social%20APP%20%E7%9C%9F%E7%9A%84%E5%A4%AA%E5%A5%BD%E7%94%A8%E4%BA%86%EF%BC%8C%E5%A4%A7%E6%8E%A8%2B1%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Cfalse%2Chi%2Chi%7Cfalse%2CHi%2CHi%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%7C",
			"AD_Custom_FB_Comment_Arr":    "true%2C98%20Social%20APP%E5%BB%A3%E5%91%8A%E6%96%87%2C%E4%BD%A0%E4%B9%9F%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%EF%BC%9F%20%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C%E5%8E%9F%E4%BE%86%E5%A4%A7%E5%AE%B6%E9%83%BD%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%20%E5%95%8A%EF%BC%81%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%20Social%20APP%20%E7%9C%9F%E7%9A%84%E5%A4%AA%E5%A5%BD%E7%94%A8%E4%BA%86%EF%BC%8C%E5%A4%A7%E6%8E%A8%2B1%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7C",
			"AD_Custom_IG_Comment_Arr":    "true%2C98%20Social%20APP%E5%BB%A3%E5%91%8A%E6%96%87%2C%E4%BD%A0%E4%B9%9F%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%EF%BC%9F%20%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C%E5%8E%9F%E4%BE%86%E5%A4%A7%E5%AE%B6%E9%83%BD%E5%9C%A8%E4%BD%BF%E7%94%A8%2098%20Social%20APP%20%E5%95%8A%EF%BC%81%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%20Social%20APP%20%E7%9C%9F%E7%9A%84%E5%A4%AA%E5%A5%BD%E7%94%A8%E4%BA%86%EF%BC%8C%E5%A4%A7%E6%8E%A8%2B1%0A%0ALine%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%EF%BC%8C%E5%BF%AB%E5%8E%BB%E8%BF%BD%E8%B9%A4%E5%90%A7%EF%BC%81%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7C",
			"Custom_IG_Comment_Arr":       "true%2C98%2BSocial%2BAPP%E5%BB%A3%E5%91%8A%E6%96%87%2C%E6%88%91%E6%9C%80%E8%BF%91%E4%BD%BF%E7%94%A8%E4%B8%80%E5%80%8B%E8%87%AA%E5%8B%95%E5%8C%96%E7%A4%BE%E4%BA%A4%E8%BC%94%E5%8A%A9APP%EF%BC%8C%E6%8E%A8%E8%96%A6%E7%B5%A6%E4%BD%A0%0A%0A98%2BSocial%2BAPP%2B%2B%E8%87%89%E6%9B%B8%E5%AE%98%E6%96%B9%E7%A4%BE%E5%9C%98%0Ahttps%3A%2F%2Fwww.facebook.com%2Fgroups%2F243243662841564%2F%0A%E7%BD%AE%E9%A0%82%E8%B2%BC%E6%96%87%E6%9C%89%E6%B4%BB%E5%8B%95%E8%B3%87%E8%A8%8A%E4%BB%A5%E5%8F%8A%E8%BC%89%E9%BB%9E%E9%8F%88%E7%B5%90%2F%E4%BD%BF%E7%94%A8%E6%95%99%E5%AD%B8%E8%88%87%E6%B5%81%E7%A8%8B%E3%80%82%0A%0ALine%E5%AE%98%E6%96%B9%E6%9C%8D%E5%8B%99%E8%99%9F%EF%BC%9A%4098-Social-APP%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%2BSocial%2BAPP%2B%2B%E6%9C%80%E8%BF%91%E4%B9%9F%E5%A4%AA%E5%A4%AF%E4%BA%86%E5%90%A7%7Ctrue%2C%E5%BB%A3%E5%91%8A%E5%88%8A%E6%9D%BF%E7%A7%9F%E5%94%AE-%E6%B4%BD%E5%AE%A2%E6%9C%8D%2C98%2BSocial%2BAPP%2B%2B%2B1%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7Cfalse%2C%2C%7C",
			"Normal_IG_Comment_Arr":       "false%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%2C%E7%A5%9D%E5%BF%AB%E6%A8%82%E5%B9%B3%E5%AE%89%7Cfalse%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%2C%E7%A5%9D%E5%A5%BD%E9%81%8B%E9%A0%86%E5%BF%83%7Cfalse%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%2C%E7%A5%9D%E9%A0%86%E5%BF%83%E5%A5%BD%E9%81%8B%7Cfalse%2Chi%2Chi%7Cfalse%2CHi%2CHi%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%BF%AB%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%2C%E5%B9%B3%E5%AE%89%E5%96%9C%E6%A8%82%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%BF%83%7Cfalse%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%2C%E5%B9%B3%E5%AE%89%E9%A0%86%E5%88%A9%7Cfalse%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%2C%E5%B9%B3%E5%AE%89%E5%81%A5%E5%BA%B7%7C%0D%0A",
			"FB_ADUser":                   "false",
		    "IG_ADUser":				   "false",
		    "Last_GhostCheckTime":		   str(time.strftime("%Y/%m/%d-%H:%M:%S")),
		    "PC_LatestUpdate":"",
			})
		return HttpResponse("OK") #帳號已存在
	except:

		return HttpResponse("Error")

def UploadSelfpage(request): #上傳個人動態首頁
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #使用者帳號
	SelfPage                         = request.GET.get("SelfPage", '') #使用者帳號
	DBController                     = MongoController().GetCursor()#取得資料庫使用權
	if Check98Login(Username,Password) == "OK": #登入成功
		User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
		DBController.update_one({  #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"SelfPage":SelfPage #自己的個人首頁
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")

def CheckUserisBuyed(request): #使用者未開通?
	Username                                         = request.GET.get("Username", '') #使用者帳號
	Password                                         = request.GET.get("Password", '') #使用者帳號
	DBController                                     = MongoController().GetCursor()#取得資料庫使用權
	
	if Check98Login(Username,Password) == "OK": #登入成功
		User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
		if DBController.find_one({"98Username": Username,"98Password":Password})["FeaturesLi"]=="":
			return HttpResponse("WaitBuyFeatures") #等待使用者開啟
		else:
			return HttpResponse("Is Buyed") #已購買了
	else:
		return HttpResponse("LoginFail")
def SyncFB_Time(request): #時間同步API
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #使用者帳號
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController                     = MongoController().GetCursor()#取得資料庫使用權
		FB_Last_StartTime=DBController.find_one({"98Username": Username,"98Password":Password},{'_id':False,"FB_Last_StartTime":1})["FB_Last_StartTime"] #返回上次開始運行的時間
		if FB_Last_StartTime=="":
			return HttpResponse("No Start Time") #沒有啟動過，所以沒有記錄時間
		year = int(FB_Last_StartTime.split("-")[0])
		mon  = int(FB_Last_StartTime.split("-")[1])
		day  = int(FB_Last_StartTime.split("-")[2].split(" ")[0])
		Hour = int(FB_Last_StartTime.split(" ")[1].split(":")[0])
		Min  = int(FB_Last_StartTime.split(":")[1])
		Sec  = int(FB_Last_StartTime.split(":")[2])
		DiffTime=abs((datetime.datetime(year,mon,day,Hour,Min,Sec) - datetime.datetime.now()).total_seconds())


		return HttpResponse(DiffTime)#將將兩個時間差相減後發給使用者
	else:
		return HttpResponse("LoginFail")

def GetOnlineCount(request): #取得上線人數
	OnlineCount=0 #上線用戶計數器
	DBController                                     = MongoController().GetCursor()#取得資料庫使用權
	for countObj in DBController.find({},{"PC_LatestUpdate":1,"FBstartClick":1}):
		try:
			_LastTime=countObj["PC_LatestUpdate"]
			year = int(_LastTime.split("/")[0])
			mon  = int(_LastTime.split("/")[1])
			day  = int(_LastTime.split("/")[2].split("-")[0])
			Hour = int(_LastTime.split("-")[1].split(":")[0])
			Min  = int(_LastTime.split("-")[1].split(":")[1])
			Sec  = int(_LastTime.split("-")[1].split(":")[2])
			#明明已開啟按讚了，卻超過一分鐘沒收到回報按讚
			if abs((datetime.datetime(year,mon,day,Hour,Min,Sec) - datetime.datetime.now()).total_seconds()/60)>3:
				pass
			else: #電腦端上線中
				if countObj["FBstartClick"]==True:
					OnlineCount+=1
		except:
			pass
	return HttpResponse(str(DBController.find({}).count())+"/"+str(OnlineCount)) #電腦是上線的
	
def GetDosInfo(request): #取得DOS視窗的運行狀態
	Username                                         = request.GET.get("Username", '') #使用者帳號
	Password                                         = request.GET.get("Password", '') #使用者帳號
	DBController                                     = MongoController().GetCursor()#取得資料庫使用權
	if Check98Login(Username,Password) == "OK": #登入成功
		FBstartClickStat=DBController.find_one({"98Username": Username,"98Password":Password},{"FBstartClick":1})["FBstartClick"]
		LastTime=DBController.find_one({"98Username": Username,"98Password":Password},{"PC_LatestUpdate":1})["PC_LatestUpdate"]
		year = int(LastTime.split("/")[0])
		mon  = int(LastTime.split("/")[1])
		day  = int(LastTime.split("/")[2].split("-")[0])
		Hour = int(LastTime.split("-")[1].split(":")[0])
		Min  = int(LastTime.split("-")[1].split(":")[1])
		Sec  = int(LastTime.split("-")[1].split(":")[2])


		#明明已開啟按讚了，卻超過一分鐘沒收到回報按讚
		if abs((datetime.datetime(year,mon,day,Hour,Min,Sec) - datetime.datetime.now()).total_seconds()/60)>15: #如果上次按讚的時間超過三分鐘了
			try:
				IsSleep=DBController.find_one({"98Username": Username,"98Password":Password})["IsSleep"]
				if IsSleep=="true": 
					return HttpResponse("Is online") #電腦是上線的 只是正在休息中
			except: #該用戶沒有IsSleep這個欄位
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"IsSleep": "false", #使用者正在休息
				  }
				}, upsert=False)
			DBController.update_one({ #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FBstartClick": False, #使用者登出系統關閉FB按讚(暫時關閉狀態)
			  }
			}, upsert=False)
			#return HttpResponse("Is online") #電腦是上線的
			return HttpResponse("Is offline") #電腦離線
		else: #電腦端上線中
			#return HttpResponse("Is offline") #電腦離線
			return HttpResponse("Is online") #電腦是上線的
	else:
		#print ("LoginFail")
		return HttpResponse("LoginFail") #電腦是上線的

def PCNowVersion(request): #取得PC版目前版本 #有版本號為正常運行  / on Fix 維修中
	return HttpResponse("v2.0.2/V2.0.3") #"v2.01/V2.0.1"
def APPNowVersion(request): #取得APP版目前版本
	return HttpResponse("v2.0.2/V2.0.2/V2.0.3/v2.0.3") #目前v2.01    #有版本號為正常運行  / on Fix 維修中
def isAlive(request): #告訴手機自己還活著
	IsSleep="false"  #此帳號正在休息
	Username                           = request.GET.get("Username", '') #使用者帳號
	Password                           = request.GET.get("Password", '') #使用者帳號
	try: #現在該帳號正在休息
		GoSleep                            = request.GET.get("GoSleep", '') #是否為休息
		IsSleep=GoSleep
	except:
		pass

	if Check98Login(Username,Password) == "OK": #登入成功
		DBController = MongoController().GetCursor()#取得資料庫使用權
		DBController.update_one({  #更新用戶資料
		  "Username": Username
		},{
		  '$set': {
			'PC_LatestUpdate': str(time.strftime("%Y/%m/%d-%H:%M:%S")),  #PC端系統狀態
			'IsSleep':IsSleep
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")
#2.01版

def GetUserInfo(request): #取得使用者資訊
	Username     = request.GET.get("Username", '') #使用者帳號
	Password     = request.GET.get("Password", '') #使用者帳號
	UUID         = request.GET.get("UUID", '') #APP登入
	PC           = request.GET.get("PC", '')  #是PC端
	DOS          = request.GET.get("DOS", '') #是PC端的DOS要來抓留言了
	DBController = MongoController().GetCursor()#取得資料庫使用權
	if (PC=="true"): #是PC端DOS畫面取得FB會員資料的
		_98UserInfo=DBController.find_one({"Username": Username,"Password":Password})
	elif (DOS=="true"):
		_98UserInfo=DBController.find_one({"Username": Username,"Password":Password})
	else:
		_98UserInfo=DBController.find_one({"98Username": Username,"98Password":Password})
	if _98UserInfo!=None:
		if UUID!="":
			if DBController.find_one({"98Username": Username})["UUID"]!="": #如果已經登入了，就會上傳UUID，但如果是空值，就是首次登入
				OldUUID=DBController.find_one({"98Username": Username})["UUID"]
				if UUID!=OldUUID: #如果新舊UUID不一樣，就是異地當入
					DBController.update_one({  #更新用戶資料
					  "98Username": Username
					},{
					  '$set': {
						"UUID":UUID #直接更新UUID到最新的，這樣舊的UUID就會自動退出了
					  }
					}, upsert=False)

					return HttpResponse("DiffLogin") #異地登入
		try:
			if (PC=="true"): #是PC端來確認的自己存在的
				DBController.update_one({  #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					'PC_LatestUpdate': str(time.strftime("%Y/%m/%d-%H:%M:%S"))  #PC端系統狀態
				  }
				}, upsert=False)
			elif (DOS=="true"):
				DBController.update_one({  #更新用戶資料
				  "Username": Username
				},{
				  '$set': {
					'PC_LatestUpdate': str(time.strftime("%Y/%m/%d-%H:%M:%S"))  #PC端系統狀態
				  }
				}, upsert=False)
			else: #只是電腦端而已
				DBController.update_one({  #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					'LatestUpdate': str(time.strftime("%Y/%m/%d-%H:%M:%S")),  #使用者登入系統(狀態)
				  }
				}, upsert=False)
		except:
			pass
		if (PC=="true"): #是PC端DOS畫面取得FB會員資料的
			UserInfo=str(DBController.find_one({"Username": Username},{'_id':False,'GhostList':False,'UserStickers':False}))#取得使用者基本資料
			UserInfo=json.dumps(UserInfo)#轉成json格式
			return HttpResponse(UserInfo.encode("utf-8"))#將使用者資料回傳回客戶端
		elif (DOS=="true"):
			UserInfo=str(DBController.find_one({"Username": Username},{'_id':False,'GhostList':False,'UserStickers':False}))#取得使用者基本資料
			UserInfo=json.dumps(UserInfo)#轉成json格式
			return HttpResponse(UserInfo.encode("utf-8"))#將使用者資料回傳回客戶端
		else:
			UserInfo=str(DBController.find_one({"98Username": Username},{'_id':False,'GhostList':False,'UserStickers':False}))#取得使用者基本資料
			UserInfo=json.dumps(UserInfo)#轉成json格式
			return HttpResponse(UserInfo.encode("utf-8"))#將使用者資料回傳回客戶端
	else:
		return HttpResponse("LoginFail")




def _98Login(request): #98帳號登入
	_98Username  = request.GET.get("_98Username", '') #使用者帳號
	_98Password  = request.GET.get("_98Password", '') #使用者帳號
	DBController = MongoController().GetCursor()#取得資料庫使用權
	#去抓取98APP帳號下面的FB資料與社團粉專網址
	_98UserInfo=DBController.find_one({"98Username": _98Username,"98Password":_98Password},{"Username":1,"Password":1,"IG_Username":1,"IG_Password":1})
	if _98UserInfo!=None:
		#將會員資訊return回去
		#for ele in DBController.find({},{"98Username":1,"_id":False}):CheckUserBuyInfo(ele["98Username"])
		CheckUserBuyInfo(_98Username) #使用98帳號去確認用戶的購買狀態是否過期

		Return98Info=_98UserInfo["Username"]+"|"+_98UserInfo["Password"]+"|"+_98UserInfo["IG_Username"]+"|"+_98UserInfo["IG_Password"]
		return HttpResponse(Return98Info)
	else:
		return HttpResponse("LoginFail")
def SetCommentStr(request): #使用者自訂留言設定
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #使用者帳號
	FB_Comment_Arr                   = request.GET.get("FB_Comment_Arr", '') #FB 自動留言語句
	IG_Comment_Arr                   = request.GET.get("IG_Comment_Arr", '') #IG 自動留言語句
	FB_Commtype                      = request.GET.get("FB_Commtype", '')#Custom/Normal 的留言
	IG_Commtype                      = request.GET.get("IG_Commtype", '')#Custom/Normal 的留言
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController=MongoController().GetCursor()#取得資料庫使用權
		UserBuyInfo     = DBController.find_one({"98Username": Username},{'_id':False,"FB_ADUser":1,"IG_ADUser":1})#取得用戶目前購買狀態是廣告用戶還是一般用戶
		AD_Com=DBController.find_one({"98Username": Username},{'_id':False,"AD_Custom_FB_Comment_Arr":1,"AD_Custom_IG_Comment_Arr":1})
		if FB_Commtype=="Custom": #用戶自訂的留言要更改
			if UserBuyInfo["FB_ADUser"]=="true": #廣告用戶
				AD_FB_write=""
				ADFB_com=AD_Com["AD_Custom_FB_Comment_Arr"]
				for ele in FB_Comment_Arr.split(",")[3:10]:
					AD_FB_write+="false,"+ele+","+ele+",|"
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"AD_Custom_FB_Comment_Arr":quote('|'.join(unquote(ADFB_com).split("|")[:3])+'|'+AD_FB_write)
				  }
				}, upsert=False)
			else: #非廣告用戶
				FB_com=""
				for ele in FB_Comment_Arr.split(","):
					FB_com+="false,"+ele+","+ele+",|"
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"Custom_FB_Comment_Arr":quote(FB_com),
					"FB_Commtype":"Custom" #FB留言狀態為自訂
				  }
				}, upsert=False)
		else:
			DBController.update_one({ #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FB_Commtype":"Normal" #FB留言狀態為預設
			  }
			}, upsert=False)

		if IG_Commtype=="Custom": #用戶自訂的留言要更改
			if UserBuyInfo["IG_ADUser"]=="true": #廣告用戶
				AD_IG_write=""
				ADIG_com=AD_Com["AD_Custom_IG_Comment_Arr"]
				for ele in IG_Comment_Arr.split(",")[3:10]:
					AD_IG_write+="false,"+ele+","+ele+",|"
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"AD_Custom_IG_Comment_Arr":quote('|'.join(unquote(ADIG_com).split("|")[:3])+'|'+AD_IG_write)
				  }
				}, upsert=False)
			else: #非廣告用戶
				IG_com=""
				for ele in IG_Comment_Arr.split(","):
					IG_com+="false,"+ele+","+ele+",|"
				DBController.update_one({ #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"Custom_IG_Comment_Arr":quote(IG_com),
				  }
				}, upsert=False)			
		else:
			DBController.update_one({ #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"IG_Commtype":"Normal" #FB留言狀態為預設
			  }
			}, upsert=False)
		DBController.update_one({ #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"FB_Comment_Arr": FB_Comment_Arr,  #FB 自動留言語句
			"IG_Comment_Arr": IG_Comment_Arr   #IG 自動留言語句
		  }
		}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端
def UserShutdown(request): #用戶關閉自動按讚了
	Username     = request.GET.get("Username", '') 
	DBController = MongoController().GetCursor()#取得資料庫使用權
	DBController.update_one({ #更新用戶資料
	  "98Username": Username
	},{
	  '$set': {
		"FBstartClick": False, #使用者登出系統關閉FB按讚(狀態)
		"LikeCount":0.0, #每次登入後都重置按讚次數
		"CommentCount":0.0 #每次登入後都重置留言次數
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端

def Logout(request): #用戶登出
	Username     = request.GET.get("Username", '') 
	DBController = MongoController().GetCursor()#取得資料庫使用權
	DBController.update_one({ #更新用戶資料
	  "98Username": Username
	},{
	  '$set': {
	  	"UserStatus":False,#登出
		"FBstartClick": False, #使用者登出系統關閉FB按讚(狀態)
		"LikeCount":0.0, #每次登出後都重置按讚次數
		"CommentCount":0.0 #每次登出後都重置留言次數
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端

def CheckIsLogin(request):#檢查使用者是否登入了
	Username                         = request.GET.get("Username", '') #使用者帳號
	DBController = MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"98Username": Username},{"UserStatus":1})["UserStatus"]==True:
		return HttpResponse("This Account is Login")#此帳號已經登入了
	else:
		return HttpResponse("Wait Login")#此等待登入


def UserCheckGhost(request): #用戶要刪除幽靈
	Username     = request.GET.get("Username", '')  
	DBController = MongoController().GetCursor()#取得資料庫使用權
	DBController.update_one({ #更新用戶資料
	  "98Username": Username
	},{
	  '$set': {
		"GhostCheck": True, #使用者刪除幽靈狀態
	  }
	}, upsert=False)
	return HttpResponse("OK")#將使用者資料回傳回客戶端

"""
def SyncField(request): #同步Field Username  到  98Username
	DBController = MongoController().GetCursor()#取得資料庫使用權
	for ele in DBController.find({},{"_id":1}):
		Username=DBController.find_one({"_id": ele["_id"]})["Username"]
		Password=DBController.find_one({"_id": ele["_id"]})["Password"]
		DBController.update_one({"_id":ele["_id"]},{'$set': {"98Username":Username,"98Password":Password}}, upsert=False)
		##print (ele)
	return HttpResponse("OK")#該用戶存在
"""
"""
def EditFeature(request): #同步Field Username  到  98Username
	DBController = MongoController().GetCursor()#取得資料庫使用權
	for ele in DBController.find({},{"_id":1}):
		try:
			if DBController.find_one({"_id":ele["_id"]},{"FeaturesLi":1})["FeaturesLi"]=="":
				DBController.update_one({"_id":ele["_id"]},{'$set': {"FeaturesLi":"FB自動幫好友按讚,2017.10.29|FB自動幫好友留言,2017.10.29|","AutoComment":True,"AutoLike":True}}, upsert=False)
		except:
			pass
		##print (ele)
	return HttpResponse("OK")#該用戶存在
"""


def CheckUserExist(request): #查找該用戶是否存在
	_98_Username     = request.GET.get("Username", '') #使用者帳號
	DBController = MongoController().GetCursor()#取得資料庫使用權
	#print (_98_Username)
	if DBController.find_one({"98Username": _98_Username})==None: #如果找不到這個使用者，代表登入錯誤
		return HttpResponse("NoExist")#該用戶不存在
	else:
		try:
			RecommendedPerson=str(DBController.find_one({"98Username": _98_Username},{'_id':False})['RecommendedPerson'])#取得使用者基本資料
		except:
			return HttpResponse("No RecommendedPerson Field")
		if (RecommendedPerson=="None"): #該用戶是首次開通的
			return HttpResponse("FirstLogin")
		else: #已登入過了
			return HttpResponse("Exist")#該用戶存在

def PostOrder(request): #發送訂單
	Username     = request.GET.get("Username", '') #使用者帳號
	OrderCode    = request.GET.get("OrderCode", '') #使用者訂單編碼
	OrderLi      = request.GET.get("OrderLi", '') #使用者訂單編碼
	OrderLevel   = request.GET.get("OrderLevel", '') #訂單購買等級
	DBController = MongoController().OrderDB()#取得訂單資料庫使用權
	while True: #產生銷售碼
		SellCode=""
		for i in range(12): #產生12位元的銷售碼
			SellCode+=random.choice(string.ascii_lowercase + string.digits)

		if DBController.find_one({"SellCode": SellCode})==None: #查找銷售碼是否有重複過了
			#未重複
			break
		#發現SellCode有重複  再次創建銷售碼
	DBController.insert_one( #創建訂單
		{
			"OrderLevel":OrderLevel, #訂單購買等級
			"OrderCreateTime":str(time.strftime("%Y/%m/%d-%H:%M:%S")),#訂單創建日期
			"98Username": Username,
			"OrderCode": OrderCode, #使用者的訂單編碼
			"OrderLi":OrderLi,#訂單內容
			"SellCode":SellCode, #唯一的銷售碼
			"FB_ADUser":"false", #非廣告用戶
			"IG_ADUser":"false", #非廣告用戶
			"IsExchange":"false",#兌換狀態
			"ExchangeTime":"", #兌換時間
		})
	return HttpResponse("OK")#該訂單已成立


def FindUserAllOrder_total(request): #搜尋該用戶的所有訂單總數
	OrderLi            = [] #多筆訂單的list
	Username           = request.GET.get("Username", '') #使用者帳號
	Order_DBController = MongoController().OrderDB()#取得訂單資料庫使用權
	try:
		OrderContent=Order_DBController.find({"98Username":Username},{"_id":False,"SellCode":False,"FB_ADUser":False,"IG_ADUser":False,"98Username":False})#訂單內容
		for OrderCont in OrderContent: #訂單陣列一個一個取出
			OrderLi.append(OrderCont)
		return HttpResponse(str(len(OrderLi)))
	except TypeError: #找不到銷售編碼
		return HttpResponse("Error not find")#沒有該銷售編碼


def FindUserAllOrder_by_ele(request): #依照訂單總數一個一個去抓取回來
	ReturnText                         = ""
	OrderLi                            = [] #多筆訂單的list
	OrderPos                           = request.GET.get("OrderPos", '') #訂單總數中的個別訂單
	Username                           = request.GET.get("Username", '') #使用者帳號
	Password                           = request.GET.get("Password", '') #使用者帳號
	if Check98Login(Username,Password) == "OK": #登入成功
		Order_DBController                 = MongoController().OrderDB()#取得訂單資料庫使用權
		try:
			OrderContent=Order_DBController.find({"98Username":Username},{"_id":False,"SellCode":False,"FB_ADUser":False,"IG_ADUser":False,"98Username":False})#訂單內容
			for OrderCont in OrderContent: #訂單陣列一個一個取出
				OrderLi.append(OrderCont)
			return HttpResponse(str(OrderLi[int(OrderPos)]).replace("{","").replace("}",""))
		except TypeError: #找不到銷售編碼
			return HttpResponse("Error not find")#沒有該銷售編碼
	else:
		return HttpResponse("LoginFail")


	


def SearchOrderCode(request): #搜尋銷售編碼
	OrderCode          = request.GET.get("OrderCode", '') #銷售編碼
	Order_DBController = MongoController().OrderDB()#取得訂單資料庫使用權
	if OrderCode=="":
		return HttpResponse("Error Not This OrederCode")#沒有該銷售編碼
	try:
		SellCode=Order_DBController.find_one({"OrderCode": OrderCode})["SellCode"]
	except TypeError: #找不到銷售編碼
		return HttpResponse("Error Not This OrederCode")#沒有該銷售編碼
	if SellCode!=None:#如果資料庫內有銷售碼
		return HttpResponse(SellCode) #返回銷售編碼


def AddFB_AccountInfo(request): #綁定FB帳號密碼
	_98Username       = request.GET.get("Username", '') #98使用者帳號
	_98Password       = request.GET.get("Password", '') #98密碼
	FBUsername        = request.GET.get("FBUsername", '') #FB使用者帳號
	FBPassword        = request.GET.get("FBPassword", '') #FB密碼
	User_DBController = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo       = User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})
	if _98UserInfo   != None:
		if _98UserInfo["Username"]=="" and _98UserInfo["Password"]=="": #用戶沒綁定過FB帳號
			User_DBController.update_one({  #更新用戶資料
			  "98Username":_98Username, #登入98帳號
			  "98Password":_98Password   #登入98密碼
			},{
			  '$set': {
			  	"Username":FBUsername, #綁定FB帳號
				"Password":FBPassword #綁定FB密碼
			  }
			}, upsert=False)
			return HttpResponse("OK")
		else:
			return HttpResponse("Exist")
	else:
		return HttpResponse("LoginFail")
def AddFanpageURL(request):
	_98Username                         = request.GET.get("Username", '') #使用者帳號
	_98Password                         = request.GET.get("Password", '') #密碼
	FanpageURL                       = request.GET.get("FanpageURL", '') #粉絲專頁URL
	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})
	if _98UserInfo!=None:
		User_DBController.update_one({  #更新用戶資料
		  "98Username": _98Username,
		  "98Password":_98Password
		},{
		  '$set': {
			"FanpageURL":FanpageURL #粉絲專頁URL
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")
def AddGroupURL(request):
	_98Username                         = request.GET.get("Username", '') #使用者帳號
	_98Password                         = request.GET.get("Password", '') #密碼
	GroupURL                         = request.GET.get("GroupURL", '') #粉絲專頁URL
	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})
	if _98UserInfo!=None:
		User_DBController.update_one({  #更新用戶資料
		  "98Username": _98Username,
		  "98Password":_98Password
		},{
		  '$set': {
			"GroupURL":GroupURL #粉絲專頁URL
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")
def GetFanpageURL(request):#取得粉絲專頁URL
	_98Username                         = request.GET.get("98Username", '') #使用者帳號
	_98Password                         = request.GET.get("98Password", '') #密碼
	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})
	if _98UserInfo!=None:
		try:
			FanpageURL=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})["FanpageURL"]
			if FanpageURL=="": #該url為空值
				raise #引發一個錯誤並回傳找不到網址的訊息
			return HttpResponse(FanpageURL)
		except:
			return HttpResponse("No find url") #找不到社團網址
	else:
		return HttpResponse("LoginFail")

def PCTraceIP(request): #追蹤PC的IP位置
	_98Username                         = request.GET.get("_98Username", '') #98使用者帳號
	IP                         = request.GET.get("IP", '') #上傳IP位置
	LoginStat                         = request.GET.get("LoginStat", '') #98密碼
	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo=User_DBController.find_one({"98Username": _98Username},{"PCLoginLog":1,"_id":False}) #檢查有沒有該98帳號
	if _98UserInfo!=None:
		User_DBController.update_one({  #更新用戶資料
		  "98Username": _98Username
		},{
		  '$set': {
			"PCLoginLog": _98UserInfo["PCLoginLog"]+IP+"|"+str(time.strftime("%Y/%m/%d-%H:%M:%S"))+"|"+LoginStat+",", #PC端登入紀錄  IP位置/時間/登入狀態
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("Not find this Account") #找不到該98帳號
def GoPCLoginLog(request): #取得PC登入紀錄
	_98Username       = request.GET.get("_98Username", '') #98使用者帳號
	IP                = request.GET.get("IP", '') #上傳IP位置
	LoginStat         = request.GET.get("LoginStat", '') #98密碼
	User_DBController = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo       = User_DBController.find_one({"98Username": _98Username},{"PCLoginLog":1,"_id":False}) #檢查有沒有該98帳號
	
	if _98UserInfo!=None:
		User_DBController.update_one({  #更新用戶資料
		  "98Username": _98Username
		},{
		  '$set': {
			"PCLoginLog": _98UserInfo["PCLoginLog"]+IP+"|"+str(time.strftime("%Y/%m/%d-%H:%M:%S"))+"|"+LoginStat+",", #PC端登入紀錄  IP位置/時間/登入狀態
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("Not find this Account") #找不到該98帳號

def ChangePassword(request):
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	NewPassword                      = request.GET.get("NewPassword", '') #新密碼
	if (NewPassword!=""):
		if CheckLogin(Username,Password) == "OK": #登入成功
			User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
			User_DBController.update_one({  #更新用戶資料
			  "Username": Username,
			  "Password":Password
			},{
			  '$set': {
				"Password":NewPassword #將功能送到使用者端的功能列表中
			  }
			}, upsert=False)
			return HttpResponse("OK")
		else:
			return HttpResponse("LoginFail")
	else:
		return HttpResponse("NewPassword is Empty")
def GetGroupURL(request):#取得社團URL
	_98Username                         = request.GET.get("98Username", '') #使用者帳號
	_98Password                         = request.GET.get("98Password", '') #密碼
	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	_98UserInfo=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})
	if _98UserInfo!=None:
		try:
			GroupURL=User_DBController.find_one({"98Username": _98Username,"98Password":_98Password})["GroupURL"]
			if GroupURL=="": #該url為空值
				raise #引發一個錯誤並回傳找不到網址的訊息
			return HttpResponse(GroupURL)
		except:
			return HttpResponse("No find url") #找不到社團網址
	else:
		return HttpResponse("LoginFail")

def CreateTask(Username,TaskDoType,Tasktarget,TaskURL,TaskURLtype,Remain_Day): #創建任務
	#  Username     使用者帳號
	#  TaskDoType   任務類型 讚(Like)/留言(Comments)/分享(Share)/追蹤(Follow)
	#  Tasktarget   任務目標做動次數
	#  TaskURL      任務目標URL
	#  TaskURLtype  任務目標URL類型 社團(Group)/個人(Self)/粉專(Fanpage)
	#  Remain_Day   任務購買天數並持續倒數
	Task_DBController = MongoController().TaskDB()#取得FB任務資料庫使用權
	Task_DBController.insert_one({
		"Username":Username,#使用者帳號
		"TaskDoType":TaskDoType,#任務類型 讚(Like)/留言(Comments)/分享(Share)/追蹤(Follow)
		"Tasktarget":int(Tasktarget),#任務目標做動次數
		"NowCount":0,#目前已做動次數
		"DoneList":"", #已做動完成過的名單
		"TaskURL":TaskURL,#任務目標URL
		"TaskURLtype":TaskURLtype,#任務目標URL類型 社團/個人/粉專
		"Remain_Day":Remain_Day,#任務剩餘天數
		})
	return "OK"

def GetTask(request): #取任務
	Username    = request.GET.get("Username", '') #使用者帳號
	Password    = request.GET.get("Password", '') #密碼
	Task_DBController = MongoController().TaskDB()#取得FB任務資料庫使用權
	if CheckLogin(Username,Password)=="OK": #登入成功
		TaskInfo = Task_DBController.find({}).sort("NowCount", 1) #找尋作動次數最低的任務
		for Taskele in TaskInfo:  
			if Taskele["Tasktarget"]-Taskele["NowCount"]<0: #檢查已按讚次數是否已達到購買標準了
				continue
			InDoneLi=False
			for DoneLi in Taskele["DoneList"].split("|"):
				if Username == DoneLi:
					InDoneLi=True #只有這邊會更改狀態
					break
			if InDoneLi==False: #已蒐尋完畢
				TaskAssigned=Task_DBController.find_one({"_id":Taskele["_id"]}) #派發任務
				return HttpResponse(str(TaskAssigned["TaskURLtype"]+"|"+TaskAssigned["TaskDoType"])+"|"+str(TaskAssigned["TaskURL"])+"|"+str(TaskAssigned["_id"]))
		return HttpResponse("No Task Assigned")#沒有任務可以指派了
	else:
		return HttpResponse("LoginFail")
def TaskReport(request): #任務回報
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	ID                               = request.GET.get("ID", '') #任務ID
	if CheckLogin(Username,Password) == "OK": #登入成功
		Task_DBController = MongoController().TaskDB()#取得FB任務資料庫使用權
		try:
			ObjectId(ID)
		except:
			return HttpResponse("Taskid error") #不是正確的任務ID
		ReportTask=Task_DBController.find_one({"_id": ObjectId(ID)})
		if ReportTask!=None:
			for DoneLi in ReportTask["DoneList"].split("|"):
				if Username == DoneLi:
					return HttpResponse("Reported") #該使用者已回報過該任務了
					break
			Task_DBController.update_one({  #更新用戶資料
			  "_id": ObjectId(ID)
			},{
			  '$set': {
			  	"DoneList":ReportTask["DoneList"]+Username+"|", #執行此次任務的使用者
				"NowCount":ReportTask["NowCount"]+1 #增加做動次數
			  }
			}, upsert=False)
			return HttpResponse("OK")
		else: #找不到該任務ID
			return HttpResponse("Not find this task") #找不到該任務
	else:
		return HttpResponse("LoginFail")
def CreateSellcode(request):
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	CodeLen                          = request.GET.get("CodeLen", '') #想要產生多少個廣告代碼
	OrderLi                          = request.GET.get("OrderLi", '') #想要產生多少個廣告代碼
	FB_ADUser 						 = request.GET.get("FB_ADUser", '') #想要產生多少個廣告代碼
	if CheckLogin(Username,Password) == "OK": #登入成功
		CodeTotal=""
		if OrderLi=="":
			OrderLi      = "AutoLike,100,1|AutoComment,50,1|"
		#OrderLi      = "AutoLike,100,1|AutoComment,50,1|"

		#OrderLi      = "AutoComment,50,0.7|FB_DetectGhost,50,0.7|"
		#OrderLi      = "AutoLike,100,12|AutoComment,50,12|FB_DetectGhost,50,12|"


		
		DBController = MongoController().OrderDB()#取得訂單資料庫使用權
		for i in range(int(CodeLen)):
			while True: #產生銷售碼
				SellCode=""
				for i in range(12): #產生12位元的銷售碼
					SellCode+=random.choice(string.ascii_lowercase + string.digits)

				if DBController.find_one({"SellCode": SellCode})==None: #查找銷售碼是否有重複過了
					#未重複
					break
				#發現SellCode有重複  再次創建銷售碼
			DBController.insert_one( #創建訂單
				{
					"Username": Username,
					"OrderCode": "", #使用者的訂單編碼
					"OrderLi":OrderLi,#訂單內容
					"SellCode":SellCode, #唯一的銷售碼
					"FB_ADUser":"false", #廣告用戶
					"IG_ADUser":"true",  #廣告用戶
					"IsExchange" : "false", #已兌換
					"ExchangeTime" : "",
					"ExchangeUser" : ""
				})
			CodeTotal+=SellCode+"|"+"\n"
		return HttpResponse(CodeTotal)#該訂單已成立
	else:
		return HttpResponse("LoginFail")
def GetSellCode(request): #使用銷售碼去更新使用者的資料表
	global Feature #將功能 True / False 列表參考進來，用以查詢開關欄位的標的
	Username           = request.GET.get("Username", '') #使用者帳號
	SellCode           = request.GET.get("SellCode", '') #銷售碼
	Order_DBController = MongoController().OrderDB()#取得訂單資料庫使用權
	Feature_li         = [] #準備要開通的功能True/False 列表
	OrderList          = Order_DBController.find_one({"SellCode": SellCode})


	User_DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	

	if SellCode=="r59ppzxa00nr":#10天的自動按讚自動留言萬能碼
		pass
	elif SellCode=="ttg3vqihexac": #1個月的自動按讚自動留言萬能碼
		pass
	elif SellCode=="vczxt52grz2h": #1個月的自動按讚自動留言幽靈偵測萬能碼
		pass
	elif SellCode=="1lpllba0kug3": #10天的自動按讚自動留言幽靈偵測萬能碼
		pass
	else:
		Order_DBController.update_one({  #更改為已兌換的狀態
		  "SellCode": SellCode
		},{
		  '$set': {
			"IsExchange":"true", #兌換狀態 (已兌換)
			"ExchangeTime":str(time.strftime("%Y/%m/%d-%H:%M:%S")),#訂單兌換時間
			"ExchangeUser":Username #填入兌換人的紀錄
		  }
		}, upsert=False)
	try:
		UserFeaturesLi     = User_DBController.find_one({"98Username": Username})["FeaturesLi"] #功能列表
		if Order_DBController.find_one({"SellCode": SellCode})["FB_ADUser"]=="true":#該訂單是廣告推薦
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FB_ADUser":"true" #廣告用戶狀態
			  }
			}, upsert=False)
		else:
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FB_ADUser":"false" #廣告用戶狀態
			  }
			}, upsert=False)
		if Order_DBController.find_one({"SellCode": SellCode})["IG_ADUser"]=="true":#該訂單是廣告推薦
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"IG_ADUser":"true" #廣告用戶狀態
			  }
			}, upsert=False)
		else:
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"IG_ADUser":"false" #廣告用戶狀態
			  }
			}, upsert=False)
	except:
		return HttpResponse("Error")#讀取功能列表發生問題
	OrderText          = "" #訂單字串

	if OrderList["IsExchange"]=="false":#如果該訂單未兌換過
		if SellCode=="8weu1akiriqp": #全功能開通碼
			Order_DBController.update_one({  #更改為已兌換的狀態
			  "SellCode": SellCode
			},{
			  '$set': {
				"IsExchange":"false", #永遠未兌換狀態 
				"ExchangeTime":str(time.strftime("%Y/%m/%d-%H:%M:%S"))#訂單兌換時間
			  }
			}, upsert=False)
		if UserFeaturesLi=="":
			for ele in ChangeKeyENG_To_CHT(OrderList["OrderLi"]).split("|"):
				if ele!="":
					Feature_li.append(Feature[ele.split(",")[0]]) #將要開通的功能填進開通列表中
					OrderText+=ele.split(",")[0]+"," #商品名稱

					today                   = time.strftime("%Y.%m.%d") #今日為起始日
					today                   = datetime.datetime.strptime(today, "%Y.%m.%d").date()
					today                   = today + datetime.timedelta(days=float(ele.split(",")[2])*31)
					if (len(ele.split(",")) == 4):
						OrderText+=str(today).replace("-",".")+"," #商品購買月份
						OrderText+=ele.split(",")[3]+"|" #該商品購買的使用人數
					else:
						OrderText+=str(today).replace("-",".")+"|" #商品購買月份


			WriteNewFeaturesName = [] #解析未開通的功能
			FeatureKeys          = [] #解析所有的功能
			Diff_Feature         = []
			Diff_Feature2        = []
			for OpenFeature in OrderText.split("|"):WriteNewFeaturesName.append(OpenFeature.split(",")[0]) 
			while '' in WriteNewFeaturesName:WriteNewFeaturesName.remove('')
			FeatureKeys   = list(Feature.keys())


			Diff_Feature  = list(set(WriteNewFeaturesName).difference(set(FeatureKeys)))
			Diff_Feature2 = list(set(FeatureKeys).difference(set(WriteNewFeaturesName)))
			
			for ele in OrderText.split("|"):
				try:
					TaskInfo=BuyOther_Feature[ele.split(",")[0]].split("|")
				except: #這個不是需要創建任務的功能
					continue
				TaskDoType  = TaskInfo[1]
				Tasktarget  = int(ele.split(",")[2].replace(".","").replace("K","00"))
				TaskURLtype = TaskInfo[3]
				Remain_Day  = ele.split(",")[1]	
				if TaskURLtype == "Self":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"SelfPage":1})["SelfPage"]
				if TaskURLtype == "Group":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"GroupURL":1})["GroupURL"]
				if TaskURLtype == "Fanpage":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"FanpageURL":1})["FanpageURL"]
				CreateTask(Username,TaskDoType,Tasktarget,TaskURL,TaskURLtype,Remain_Day)
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FeaturesLi":OrderText #將功能送到使用者端的功能列表中
			  }
			}, upsert=False)

			for Feature_ele in Feature_li: #讀取開通列表功能
				User_DBController.update_one({  #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					Feature_ele:True #批次開通功能
				  }
				}, upsert=False)
			return HttpResponse("OK")#輸入資料成功

		else: #已有購買過了

			Feature_Text = "";#準備寫入更新的功能字串
			NewFeatureLi = []

			OldFeature   = UserFeaturesLi.split("|") #已購買的功能

			while '' in OldFeature:
				OldFeature.remove('')

			#先只更新舊的功能到期時間
			for Feature_item in UserFeaturesLi.split("|"):
				if Feature_item!="":
					Feature_Name=Feature_item.split(",")[0]  #將功能名稱從功能列表剖析出來
					for ele in ChangeKeyENG_To_CHT(OrderList["OrderLi"]).split("|"):
						if ele!="":
							if Feature_Name in ele.split(",")[0]: #更新已購買的功能
								OldFeature.remove(Feature_item)
								FeatureTime = Feature_item.split(",")[1] #將目前服務的到期時間抓出來
								BuyMon =float(ele.split(",")[2]) #購買月份


								Feature_Day_Li=[]

								try:
									if Feature_item.split(",")[1]!="false":
										for FeatureDay in Feature_item.split(",")[1].split("."):
											Feature_Day_Li.append(int(FeatureDay))


										FeatureDay    = datetime.date(Feature_Day_Li[0],Feature_Day_Li[1],Feature_Day_Li[2]) #功能到期日
										FeatureDay    = FeatureDay+datetime.timedelta(days=BuyMon*31)#將目前功能的到期日加上這次購買的日期延長
										FeatureDay    = str(FeatureDay).replace("-",".")
										Feature_Text += Feature_Name+","+FeatureDay+"|"
								except:
									pass


			NewOrderLi  = [] #新功能的list
			DiffResult  = []
			DiffResult2 = []
			checkDiff_1 = []
			checkDiff_2 = []

			for FeatureEle in Feature_Text.split("|"):
				checkDiff_1.append(FeatureEle.split(",")[0])
				
			for OrderListEle in ChangeKeyENG_To_CHT(OrderList["OrderLi"]).split("|"):
				checkDiff_2.append(OrderListEle.split(",")[0])

			DiffResult=list(set(checkDiff_2).difference(set(checkDiff_1)))
			DiffResult2=list(set(checkDiff_1).difference(set(checkDiff_2)))
			DiffResult.extend(DiffResult2)

			while '' in DiffResult:
				DiffResult.remove('')
			
			for CheckNew in DiffResult:
				for ele in ChangeKeyENG_To_CHT(OrderList["OrderLi"]).split("|"):
					if ele.split(",")[0]==CheckNew:
						today = time.strftime("%Y.%m.%d") #今日為起始日
						today = datetime.datetime.strptime(today, "%Y.%m.%d").date()
						today = today + datetime.timedelta(days=float(ele.split(",")[2])*31)
						NewOrderLi.append(ele.split(",")[0]+","+str(today).replace("-","."))

			#寫入訂單字串
			WriteNewFeaturesLi=Feature_Text+"||"+'||'.join(OldFeature)+"||"+'||'.join(NewOrderLi)
			WriteNewFeaturesLi.replace("||","|")

			newWriteLi=WriteNewFeaturesLi.split("|")
			while '' in newWriteLi:  #清空  list的 " "空內容
				newWriteLi.remove('')

			WriteNewFeaturesLi="|".join(newWriteLi)+"|"



			WriteNewFeaturesName=[] #解析未開通的功能
			
			#輸出功能內容
			for OpenFeature in WriteNewFeaturesLi.split("|"):WriteNewFeaturesName.append(OpenFeature.split(",")[0]) 
			
			#刪除list空值
			while '' in WriteNewFeaturesName:WriteNewFeaturesName.remove('')
			
			for ele in ChangeKeyENG_To_CHT(OrderList["OrderLi"]).split("|"):
				if (len(ele.split(","))==4):
					try:
						indexPos           = WriteNewFeaturesLi.index(ele.split(",")[0])+len(ele.split(",")[0])+11 #因為2018.XX.XX共11個字元
						WriteNewFeaturesLi = WriteNewFeaturesLi.replace(WriteNewFeaturesLi[:indexPos],WriteNewFeaturesLi[:indexPos]+","+ele.split(",")[3]+"|")
						WriteNewFeaturesLi.replace("||","|")
					except ValueError:
						continue
			#排序
			TempSort=[]
			New_WriteNewFeaturesLi=WriteNewFeaturesLi.split("|")
			while '' in New_WriteNewFeaturesLi:
				New_WriteNewFeaturesLi.remove('')
			for ele in New_WriteNewFeaturesLi:
				TempSort.append(FeatureTheKeys.index(ele.split(",")[0]))

			TempSort.sort()
			resultSort=[]
			for IndexPos in TempSort:
				for ele2 in New_WriteNewFeaturesLi:
					if FeatureTheKeys.index(ele2.split(",")[0])==IndexPos:
						resultSort.append(ele2)
					


			ExitOrderText='|'.join(resultSort)+"|" #要寫回資料表的功能
			for ele in ExitOrderText.split("|"): #找尋須創建任務的功能
				try:
					TaskInfo=BuyOther_Feature[ele.split(",")[0]].split("|")
				except: #這個不是需要創建任務的功能
					continue
				TaskDoType  = TaskInfo[1]
				Tasktarget  = int(ele.split(",")[2].replace(".","").replace("K","00"))
				TaskURLtype = TaskInfo[3]
				Remain_Day  = ele.split(",")[1]	
				if TaskURLtype == "Self":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"SelfPage":1})["SelfPage"]
				if TaskURLtype == "Group":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"GroupURL":1})["GroupURL"]
				if TaskURLtype == "Fanpage":
					TaskURL=User_DBController.find_one({"98Username": Username},{'_id':False,"FanpageURL":1})["FanpageURL"]
				CreateTask(Username,TaskDoType,Tasktarget,TaskURL,TaskURLtype,Remain_Day)

	
			User_DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
				"FeaturesLi":ExitOrderText #將功能送到使用者端的功能列表中
			  }
			}, upsert=False)

			for Feature_ele in WriteNewFeaturesLi.split("|"): #讀取開通列表功能
				if Feature_ele!="":
					if Feature_ele.split(",")[1]!="false":
						Feature_li.append(Feature[Feature_ele.split(",")[0]]) #將要開通的功能填進開通列表中



			for Feature_ele in Feature_li:
				User_DBController.update_one({  #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					Feature_ele:True #批次開通功能
				  }
				}, upsert=False)
		
			return HttpResponse("OK")#輸入資料成功
	else:
		return HttpResponse("Error Not This SellCode")#沒有該銷售編碼
def CheckUserBuyInfo(Username): #功能回收系統
	global Feature #將功能 True / False 列表參考進來，用以查詢開關欄位的標的
	DBController  = MongoController().GetCursor()#取得用戶資料庫使用權	
	ToggleFeature = [] #準備要開關的功能	
	FeaturesLi    = DBController.find_one({"98Username": Username})["FeaturesLi"]
	today         = time.strftime("%Y.%m.%d") #與今日比對
	today         = datetime.datetime.strptime(today, "%Y.%m.%d").date()
	for Feature_ele in FeaturesLi.split("|"): #讀取已開通列表的功能
		if Feature_ele!="":
			datetime.date.today()
			# maturityDay=到期日
			maturityDay=datetime.datetime(int(Feature_ele.split(",")[1].split(".")[0]),int(Feature_ele.split(",")[1].split(".")[1]),int(Feature_ele.split(",")[1].split(".")[2]))
			if datetime.datetime.now()> maturityDay: #當前日期大於到期日  =  過期了
				ToggleFeature.append(Feature[Feature_ele.split(",")[0]]) #將要變動的功能填進開通列表中
				#f=open("Feature.txt","a")
				#f.write("\n")
				#f.write("-------------------------------------------------------------------------------------------------------")
				#f.write("\n")
				#f.write(str("Username:"+Username+" FeatureName:"+Feature[Feature_ele.split(",")[0]]+"到期日:"+str(maturityDay)))
				#f.write("\n")
				#f.write("-------------------------------------------------------------------------------------------------------")
				#f.write("\n")
				#f.close()
				##print ("Username:"+Username+" FeatureName:"+Feature[Feature_ele.split(",")[0]]+"到期日:"+str(maturityDay))
	#if len(ToggleFeature)>0:
	#	ToggleFeature=list(Feature.values())
	NewFeaturesLi=FeaturesLi.split("|")
	for search_value in ChangeKeyENG_To_CHT('|'.join(ToggleFeature)).split("|"):
		for key, value in Feature.items():
			if ChangeKeyENG_To_CHT(value) == search_value:
				for ele in NewFeaturesLi:
					if key==ele.split(",")[0]:
						NewFeaturesLi.remove(ele)

	f=open("Feature.txt","a")
	f.write(str(str(NewFeaturesLi).encode("utf-8")))
	f.write("\n")
	f.write(Username)
	f.write("\n")
	f.close()
	##print (Username)
	##print (NewFeaturesLi)
	DBController.update_one({  #更新用戶資料
	  "98Username": Username
	},{
	  '$set': {
		"FeaturesLi":'|'.join(NewFeaturesLi) #將功能送到使用者端的功能列表中
	  }
	}, upsert=False)
	for Freature_li in ToggleFeature:
		DBController.update_one({  #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			Freature_li:False #批次開通功能
		  }
		}, upsert=False)
def CheckLogin(Username,Password): #檢查該帳號是否存在
	DBController=MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"Username": Username,'Password':Password})==None:
		return "LoginFail" #登入拒絕
	else:
		return "OK" #登入成功


def Check98Login(Username,Password): #檢查該98帳號是否存在
	DBController=MongoController().GetCursor()#取得資料庫使用權
	if DBController.find_one({"98Username": Username,'98Password':Password})==None:
		return "LoginFail" #登入拒絕
	else:
		return "OK" #登入成功
def CantLogin(request):
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	DBController=MongoController().GetCursor()#取得資料庫使用權
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController.update_one({  #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
			"CanLogin":False #無法登入
		  }
		}, upsert=False)
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")


def CheckCanLogin(request):
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	if Check98Login(Username,Password) == "OK": #登入成功
		if DBController.find_one({"98Username": Username,'98Password':Password})["CanLogin"]==True:
			pass
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")

def CheckFB_is_Click(request):# 檢查FB按讚是否啟動
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	DBController = MongoController().GetCursor()#取得資料庫使用權
	if Check98Login(Username,Password) == "OK": #登入成功
		FbClick_Status=DBController.find_one({"98Username": Username,'98Password':Password},{"FBstartClick":1})["FBstartClick"]
		FB_Last_StartTime=DBController.find_one({"98Username": Username,'98Password':Password},{"FB_Last_StartTime":1})["FB_Last_StartTime"]
		return HttpResponse(str(FbClick_Status)+"|"+str(FB_Last_StartTime))
	else:
		return HttpResponse("LoginFail") #FB尚未啟動按讚

def StartFB_Click(request):# 開始FB按讚
	Username                         = request.GET.get("Username", '') #使用者帳號
	Password                         = request.GET.get("Password", '') #密碼
	DBController = MongoController().GetCursor()#取得資料庫使用權
	if Check98Login(Username,Password) == "OK": #登入成功
		DBController.update_one({  #更新用戶資料
		  "98Username": Username
		},{
		  '$set': {
		  	"FB_Last_StartTime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #更新這次啟動的時間
			"FBstartClick": True,  #使用者開始FB按讚(狀態)
			"LikeCount":0.0, #每次登入後都重置按讚次數
			"CommentCount":0.0 #每次登入後都重置留言次數
		  }
		}, upsert=False)
		
		return HttpResponse("OK")
	else:
		return HttpResponse("LoginFail")

@csrf_exempt
def Start_Click(request): #User 登入
	Username     = request.GET.get("Username", '') #使用者帳號
	Password     = request.GET.get('Password', '') 
	UUID         = request.GET.get('UUID', '') 
	DBController = MongoController().GetCursor()#取得資料庫使用權
	try:
		if DBController.find_one({"98Username": Username,'98Password':Password})["ServiceAccount"]==True:
			return HttpResponse("ServiceAccount")#客服帳戶
	except:
		pass

	if DBController.find_one({"98Username": Username,'98Password':Password})==None:
	 #如果找不到這個使用者，代表登入錯誤
		#print ("LoginFail")
		return HttpResponse("LoginFail")#登入失敗

	elif DBController.find_one({"98Username": Username,'98Password':Password})["ServiceAccount"]==False: #非客服帳戶
		if UUID!="": #如果使用者是用APP登入，就會發送UUID
			if DBController.find_one({"98Username": Username,'98Password':Password})["UUID"]!="": #如果已經登入了，就會上傳UUID，但如果是空值，就是首次登入
				OldUUID=DBController.find_one({"98Username": Username,'98Password':Password})["UUID"]
				if UUID!=OldUUID: #如果新舊UUID不一樣，就是異地當入
					DBController.update_one({  #更新用戶資料
					  "98Username": Username
					},{
					  '$set': {
						"UUID":UUID #直接更新UUID到最新的，這樣舊的UUID就會自動退出了
					  }
					}, upsert=False)

					return HttpResponse("DiffLogin") #異地登入

			if DBController.find_one({"98Username": Username,'98Password':Password})["UUID"]=="": #如果目前該帳戶沒有UUID
				DBController.update_one({  #更新用戶資料
				  "98Username": Username
				},{
				  '$set': {
					"UUID":UUID, #將目前的UUID變成最新的UUID
				  }
				}, upsert=False)


		#如果使用者已經登入過了，不能算是重複登入
		if DBController.find_one({"98Username": Username,'98Password':Password},{"UserStatus":1})["UserStatus"]==True:
			return HttpResponse("OK")#登入成功
		else:
			DBController.update_one({  #更新用戶資料
			  "98Username": Username
			},{
			  '$set': {
			  	"FB_Last_StartTime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #更新這次啟動的時間
				"UserStatus": True,  #使用者登入系統(狀態)
			  }
			}, upsert=False)
		
		return HttpResponse("OK")#登入成功
