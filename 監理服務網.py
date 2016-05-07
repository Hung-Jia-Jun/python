#-*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests,urllib2
files={
"memberId":"A126501825",
"stationCode":"20",
"plateType":"1",
"method":"step2",
"ownerType":"1",
"processType":"2",
"hasGetPlate":"N",
"countyText":"基隆市",
"area":"仁愛區",
"zipCode":"200",
"county":"",
"location":"",
"orignPlateNo":"",
"seriesNoType":"1",
"carSeriesNo":"WDD2052451F331252",
"bodyNo":"",
"engineNo":"",
"ownerName":"AFAF",
"ownerUid":"A129162302",
"CSRFToken":"1148bc5c-231f-4d88-a9b7-7f17ca5e847b",
} 
GetCookie={
    "DWRSESSIONID":"4yFbuMvFACAPIchVjAXPyUAeail",
    "MVDAUTH":"TGT-57-fEeMbxtBPLHtfa3zhbRcejLRYXUPjhqIeXs02fIa5xQDvACEH4-www.mvdis.gov.tw",
    "M3UID":"A126501825",
    "BSESSIONID1":"A7FD509506333A6CB341416AC96CD573.tsb11",
    "_gat":"1",
    "JSESSIONID3":"E221F4B060D677896D7F2524A32384A8.tsp72",
    "JSESSIONID1":"004BF1A6BA34D15EBF7A6E7DE1B74B41.tsp12",
    "_ga":"GA1.3.224652041.1462607619",
    "M3UID":"A126501825"
}
header={
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
}
s=requests.Session()
s.headers.update({'Referer':"https://www.mvdis.gov.tw/m3-emv-plate/webpickno/queryPickNo" })
res=s.post("https://www.mvdis.gov.tw/m3-emv-plate/webpickno/member/operatePickNo#anchor",headers=header,data=files,cookies=GetCookie,verify=False)
soup = BeautifulSoup(res.text,"html.parser")
print soup.text
