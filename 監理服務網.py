#-*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests,urllib2
files={
"plateNo":"1753-S5",
"price":"2000",
"method":"step1",
"keepQryData":"",
"CSRFToken":"6089a1ae-3855-4481-9448-8be02d11f1af",
} 
GetCookie={
    "DWRSESSIONID":"FCqW9jUVXkE$fMklYURPStib5il",
    "_gat":"1",
    "JSESSIONID3":"88D261EE1C4274C66C5A5B701B8C8EDA.tsp72",
    "BSESSIONID1":"B3201A4CC3940A0D6CB9A7F682F72188.tsb12",
    "MVDAUTH":"TGT-422-chclhmpY2IE0fjmmsdypDzI0oqGxJOdpbdOfKPaIUZZgae96xx-www.mvdis.gov.tw",
    "M3UID":"A126501825",
    "JSESSIONID1":"C526E7140D02B4E812B70B85341EB87D.tsp12",
    "_ga":"GA1.3.857149626.1462496845",
    "M3UID":"A126501825"
}
s=requests.Session()

res=s.post("https://www.mvdis.gov.tw/m3-emv-plate/webpickno/member/operatePickNo#anchor",files=files,cookies=GetCookie,verify=False)
soup = BeautifulSoup(res.text,"html.parser")
print soup.text
