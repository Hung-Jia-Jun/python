# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import datetime, time,sys
import requests
print u"請輸入股票代號"
def CheckBoolinger(OpenPrice):
	if float(OpenPrice)>float(Bollinger_Bands_Topcut):
		print u"開盤價已突破壓力線該出場或是要加碼了!!!"
	else:
		print u"請繼續持倉"
	if float(HightPrice)>float(Bollinger_Bands_Topcut):
		print u"最高價已突破壓力線該出場了!!!"
	else:
		print u"請繼續持倉"
	if float(HightPrice)>float(Bollinger_Bands_Topcut):
		print u"該出場了!!!"
	else:
		print u"請繼續持倉"
	#float(HightPrice)
	#(LowPrice)
	pass
StockSetNo = raw_input("").decode(sys.stdin.encoding)
payload = {"StockNo":StockSetNo,"Kcounts":"1","Type":"%E6%97%A5K_%E5%B8%83%E6%9E%97%E9%80%9A%E9%81%93%7C"}
res=requests.get('http://w.wantgoo.com/Stock/%E5%80%8B%E8%82%A1%E7%B7%9A%E5%9C%96/%E6%8A%80%E8%A1%93%E7%B7%9A%E5%9C%96%E8%B3%87%E6%96%99Multi',params=payload)
resSpilt=res.text
Bollinger_Bands_Mid=resSpilt.split(';')[0]
Bollinger_Bands_Top=resSpilt.split(';')[1]
Bollinger_Bands_Down=resSpilt.split(';')[2]
Bollinger_Bands_Midcut=Bollinger_Bands_Mid[99:105]
Bollinger_Bands_Topcut=Bollinger_Bands_Top[37:42]
Bollinger_Bands_Downcut=Bollinger_Bands_Down[37:42]
if float(Bollinger_Bands_Topcut)<100:
	Bollinger_Bands_Midcut=Bollinger_Bands_Mid[99:103]
print u"今日布林通道壓力線",float(Bollinger_Bands_Topcut)
print u"今日布林通道中線",float(Bollinger_Bands_Midcut)
print u"今日布林通道支撐線",float(Bollinger_Bands_Downcut)
soup = BeautifulSoup(res.text,"html.parser")
payload2={"StockNo":StockSetNo,"Kcounts":"1","Type":"%E6%97%A5K_K%E7%B7%9A%7C"}
res2=requests.get("http://w.wantgoo.com/Stock/%E5%80%8B%E8%82%A1%E7%B7%9A%E5%9C%96/%E6%8A%80%E8%A1%93%E7%B7%9A%E5%9C%96%E8%B3%87%E6%96%99Multi",params=payload2)
res2Spilt=res2.text
OpenPrice=res2Spilt.split(':')[6]
OpenPrice=OpenPrice[0:4]
HightPrice=res2Spilt.split(':')[7]
HightPrice=HightPrice[0:4]
LowPrice=res2Spilt.split(':')[8]
LowPrice=LowPrice[0:4]
if Bollinger_Bands_Midcut>99:
	OpenPrice=OpenPrice[0:3]
	HightPrice=HightPrice[0:3]
	LowPrice=LowPrice[0:3]
if Bollinger_Bands_Midcut<99:
	OpenPrice=OpenPrice[0:3]
	HightPrice=HightPrice[0:3]
	LowPrice=LowPrice[0:3]

print u"今日開盤價:",float(OpenPrice)
print u"今日最高價:",float(HightPrice)
print u"今日最低價",float(LowPrice)
OpenPriceCheck=float(OpenPrice)
CheckBoolinger(OpenPriceCheck)


"""
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
file_name = "ScreenShot" + st + ".png"
time.sleep(5)
browser.save_screenshot(file_name)
print u"截圖成功!!!"
"""


    
