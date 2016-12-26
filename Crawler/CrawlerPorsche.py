import requests
from Floder_rename import *
from bs4 import BeautifulSoup
from tqdm import *

def CityToGPS(City):
	Parameter = {'ak':'B74b66c16dece8bc726d25dcf77b6399','output':'json','address':City}
	r = requests.post('http://api.map.baidu.com/geocoder/v2/',data=Parameter)
	return r.json()["result"]["location"]["lat"],r.json()["result"]["location"]["lng"]

def TryExcept(address,name):
	returnStr=""
	try:
		returnStr=str(address.find(name)).split(">")[1].split("<")[0]
		return returnStr
	except IndexError:
		return ""
def StoreSearch(City,lat,lng):
	ReturnJson=""
	url="http://www.porsche.com/all/dealer2/GetLocationsWebService.asmx/GetLocationsInStateSpecialJS?market=china&siteId=china&language=zh&state=&_locationType=Search.LocationTypes.Dealer&searchMode=proximity&searchKey="+str(lat)+"%7C"+str(lng)+"&address="+City+"&maxproximity=&maxnumtries=&maxresults="
	r = requests.get(url)
	#print r.text
	soup = BeautifulSoup(r.text,"html.parser")

	for address in soup.find_all("location"):
		ReturnJson+="{"+'''"'''+"name"+'''"'''+":"+'''"'''+TryExcept(address,"name")+'''"'''+","
		ReturnJson+='''"postcode'''+'''":"'''+TryExcept(address,"postcode")+'''"'''+","
		ReturnJson+='''"city'''+'''":"'''+TryExcept(address,"city")+'''"'''+","
		ReturnJson+='''"street'''+'''":"'''+TryExcept(address,"street")+'''"'''+","
		ReturnJson+='''"phone'''+'''":"'''+TryExcept(address,"phone")+'''"'''+","
		ReturnJson+='''"fax'''+'''":"'''+TryExcept(address,"fax")+'''"'''+"},"
	return ReturnJson

OutputJson="["
Write_txt=Write_txt("C:/Python27/Scripts/CrawlerPosche/City_result.txt")
Write_txt.Write_Action("[")
Text_str=Read_txt("C:/Python27/Scripts/CrawlerPosche/City.txt")
for text in tqdm(Text_str):
	lat,lng=CityToGPS(text)
	OutputJson=StoreSearch(text,lat,lng)
	Write_txt.Write_Action(OutputJson)

Write_txt.CloseFile()
#Text_str=Read_txt("C:/Python27/Scripts/CrawlerPosche/City.txt")
#Text_str=''.join(Text_str)
#Write_txt("C:/Python27/Scripts/CrawlerPosche/City_result.txt",Text_str[:-1]+"]")
