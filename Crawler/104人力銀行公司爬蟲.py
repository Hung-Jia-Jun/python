import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import sys

import pdb


download_dir = "Export.csv" #where you want the file to be downloaded to 

csv = open(download_dir, "w+") 
#"w" indicates that you're writing strings to the file

#定義CSV資料欄位
columnTitleRow = "公司名稱,產業別, 產業說明, 員工人數, 資本額, 聯絡人, 地址, 電話, 傳真, 公司網址, 公司簡介, 商品與服務\n"
csv.write(columnTitleRow)
csv.close()


#設定Session與header
s = requests.Session()
s.headers.update({"Referer":"https://www.104.com.tw/cust/list/index/?page=4&area=6001001009,6001001008&order=1&mode=s&jobsource=checkc",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"})


#先爬取士林北投區的公司列表
req = s.get("https://www.104.com.tw/cust/list/ajax/index?page=4&area=6001001009,6001001008&order=1&mode=s&jobsource=checkc")
req.encoding = 'UTF-8'
JsonStr=req.text
json = json.loads(JsonStr)

#目標公司詳細資料網頁
cusBaseUrl="https://www.104.com.tw/jobbank/custjob/index.php?r=cust&j="
for ele in json['data']['list']:
    公司名稱=""
    產業別=""
    產業說明=""
    員工人數=""
    資本額=""
    聯絡人=""
    地址=""
    電話=""
    傳真=""
    公司網址=""
    公司簡介=""
    商品與服務=""
    Custom_reqUrl=""
    csv = open(download_dir, "a+") 
    Custom_reqUrl=cusBaseUrl+ele['custUrl'].split("c/")[1]
    CustomDetail=s.get(Custom_reqUrl)
    CustomDetail.encoding = 'UTF-8'
    
    
    selector = etree.HTML(CustomDetail.text)

    divs = selector.xpath(' //*[@id="intro"]/p/text()')
    公司簡介=""
    for ele in divs:
        公司簡介+=ele

    divs = selector.xpath('//*[@id="intro"]/div[1]/p/text()')
    商品與服務=""
    row=""
    for ele in divs:
        商品與服務+=ele
        
        
        
    soup = BeautifulSoup(CustomDetail.text, 'html.parser')
    公司名稱=soup.find_all('h1')[0].text
    
    if "祥瑞醫管專注於兩岸醫護管理交流與培訓" in 公司名稱:
        pdb.set_trace()
    if "104人力銀行" in 公司名稱:
        continue
        
    print (公司名稱)
    
    num=0
    for ele in soup.find_all('dd'):
        num+=1
        if num==1:
            產業別=ele.text
        if num==2:
            產業說明=ele.text
        if num==3:
            員工人數=ele.text
        if num==4:
            資本額=ele.text
        if num==5:
            聯絡人=ele.text
        if num==6:
            地址=ele.text.split("地圖")[0]
        if num==7:
            電話=ele.text
            if "暫不提供" not in 電話:
                try:
                    電話=ele.img.get('src').split("Text=")[1]
                except:
                    電話="暫不提供"
        if num==8:
            傳真=ele.text
        if num==9:
            公司網址=ele.text
            if 'http' not in 公司網址:
                if 'com' not in 公司網址:
                    公司網址="暫不提供"
                    
    公司名稱=公司名稱.replace(",","，")
    產業別=產業別.replace(",","，")
    產業說明=產業說明.replace(",","，")
    員工人數=員工人數.replace(",","，")
    資本額=資本額.replace(",","，")
    聯絡人=聯絡人.replace(",","，")
    地址=地址.replace(",","，")
    電話=電話.replace(",","，")
    傳真=傳真.replace(",","，")
    公司網址=公司網址.replace(",","，")
    公司簡介=公司簡介.replace(",","，")
    商品與服務=商品與服務.replace(",","，")
    row =  公司名稱+','+產業別+','+ 產業說明+','+ 員工人數+','+ 資本額+','+ 聯絡人+','+ 地址+','+ 電話+','+ 傳真+','+ 公司網址+','+ 公司簡介+','+ 商品與服務
    print (Custom_reqUrl, 商品與服務)
    row=row.replace("\n","").replace("\r","")
    csv.write(row.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
    csv.write("\n")

    csv.close()
