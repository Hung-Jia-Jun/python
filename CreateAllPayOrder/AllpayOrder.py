# -*- coding: utf-8 -*-
import requests,pdb,time,random,json
from urllib.parse import quote
from urllib.parse import unquote
from datetime import datetime
import hashlib
from rfc3986 import uri_reference
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

MerchantID="2000132"
HashKey="5294y06JbISpM5x9" #kAMHRofSuzRM9Wbp
HashIV="v77hoKGq4kWxNNIS" #jKkwpGAXU5b2Umqu
TradeDesc="建立超商代碼測試訂單"
TotalAmount="31"
ReturnURL="https://developers.allpay.com.tw/AioMock/MerchantReturnUrl"
ClientBackURL="https://developers.allpay.com.tw/AioMock/MerchantClientBackUrl"
ItemName="MacBook 30元X2#iPhone6s 40元X1"
MerchantTradeDate=str(time.strftime("%Y/%m/%d %H:%M:%S"))
MerchantTradeNo="DX2017102601490783f0"

OrderStr="ChoosePayment=CVS&ChooseSubPayment=CVS&ClientBackURL="+ClientBackURL+"&ItemName="+ItemName+"&MerchantID="+MerchantID+"&MerchantTradeDate="+MerchantTradeDate+"&MerchantTradeNo="+MerchantTradeNo+"&PaymentType=aio&ReturnURL="+ReturnURL+"&StoreID=&TotalAmount="+TotalAmount+"&TradeDesc="+TradeDesc
CheckValue="HashKey"+HashKey+"&"+OrderStr+"&"+HashIV
CheckValue=quote(CheckValue).lower()

print (CheckValue)

CheckValue.replace('''-''','''-''')	
CheckValue.replace('''_''','''_''')	
CheckValue.replace('''.''','''.''')	
CheckValue.replace('''!''','''!''')	
CheckValue.replace('''%7e''','''~''')	
CheckValue.replace('''*''','''*''')	
CheckValue.replace('''(''','''(''')	
CheckValue.replace(''')''',''')''')	
CheckValue.replace('''+''',''' ''')	
CheckValue.replace('''40%''','''@''')	
CheckValue.replace('''23%''','''#''')	
CheckValue.replace('''24%''','''$''')	
CheckValue.replace('''25%''','''%''')	
CheckValue.replace('''%5e''','''^''')	
CheckValue.replace('''26%''','''&''')	
CheckValue.replace('''%3d''','''=''')	
CheckValue.replace('''%2b''','''+''')	
CheckValue.replace('''%3b''',''';''')	
CheckValue.replace('''%3f''','''?''')	
CheckValue.replace('''%2f''','''/''')	
CheckValue.replace('''%5c''','''\\''')	
CheckValue.replace('''%3e''','''>''')	
CheckValue.replace('''%3c''','''<''')	
CheckValue.replace('''25%''','''%''')	
CheckValue.replace('''60%''','''`''')	
CheckValue.replace('''%5b''','''[''')	
CheckValue.replace('''%5d''',''']''')	
CheckValue.replace('''%7b''','''{''')	
CheckValue.replace('''%7d''','''}''')	
CheckValue.replace('''%3a''',''':''')	
CheckValue.replace('''27%''','''\'''')	
CheckValue.replace('''22%''','''"''')	
CheckValue.replace('''%2c''',''',''')	
CheckValue.replace('''%7c''','''|''')	
print (CheckValue)
pdb.set_trace()
CheckValue=hashlib.sha256(CheckValue.encode("utf-8")).hexdigest().upper()
print (CheckValue)

payload = {
	"MerchantID":MerchantID,
	"HashKey":HashKey,
	"HashIV":HashIV,
	"TradeDesc":TradeDesc,
	"TotalAmount":TotalAmount,
	"ReturnURL":ReturnURL,
	"ClientBackURL":ClientBackURL,
	"ItemName":ItemName,
	"MerchantTradeDate":MerchantTradeDate,
	"MerchantTradeNo":MerchantTradeNo,
}
ALLPAYURL="https://payment-stage.allpay.com.tw/Cashier/AioCheckOut/V4"
#req=requests.post(ALLPAYURL, params=payload)


options = Options()
options.add_argument("--disable-notifications") #禁用通知
options.add_argument("--mute-audio") #禁用聲音
options.add_argument("--disable-gpu") #禁用GPU渲染

options.add_argument("--disable-infobars")  #關閉黃色的提醒  "瀏覽器正被自動測試軟體控制中"
driver=webdriver.Chrome(os.getcwd() + "/WebDriver/chromedriver.exe", chrome_options=options)
driver.get("file:///D:/Users/Jason/AppData/Local/Programs/Python/Python36-32/Scripts/FacebookClickLike/Order.html")


driver.find_elements_by_name("MerchantID")[0].clear()
driver.find_elements_by_name("MerchantTradeNo")[0].clear()
driver.find_elements_by_name("MerchantTradeDate")[0].clear()
driver.find_elements_by_name("TotalAmount")[0].clear()
driver.find_elements_by_name("TradeDesc")[0].clear()
driver.find_elements_by_name("ItemName")[0].clear()
driver.find_elements_by_name("ReturnURL")[0].clear()
driver.find_elements_by_name("ClientBackURL")[0].clear()
driver.find_elements_by_name("CheckMacValue")[0].clear()

driver.find_elements_by_name("MerchantID")[0].send_keys(MerchantID)
driver.find_elements_by_name("MerchantTradeNo")[0].send_keys(MerchantTradeNo)
driver.find_elements_by_name("MerchantTradeDate")[0].send_keys(MerchantTradeDate)
driver.find_elements_by_name("TotalAmount")[0].send_keys(TotalAmount)
driver.find_elements_by_name("TradeDesc")[0].send_keys(TradeDesc)
driver.find_elements_by_name("ItemName")[0].send_keys(ItemName)
driver.find_elements_by_name("ReturnURL")[0].send_keys(ReturnURL)
driver.find_elements_by_name("ClientBackURL")[0].send_keys(ClientBackURL)
driver.find_elements_by_name("CheckMacValue")[0].send_keys(CheckValue)
#pdb.set_trace()
#driver.find_elements_by_name("送出訂單")[0].click()