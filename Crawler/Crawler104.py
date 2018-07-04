
# coding: utf-8

# In[1]:


# coding: utf-8
import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import sys
import time
import pdb
from tqdm import tqdm_notebook
from tqdm import tqdm as CMDtqdm
import codecs


#設定Session與header
s = requests.Session()
s.headers.update({"Referer":"https://www.104.com.tw/cust/list/index/?page=4&area=6001001009,6001001008&order=1&mode=s&jobsource=checkc",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"})
#目標公司詳細資料網頁
cusBaseUrl="https://www.104.com.tw/jobbank/custjob/index.php?r=cust&j="



#總公司頁數的所有公司列表
Company_jsonLi=[]

AreaLi=["6001001009",
"6001001008",
"6001002026",
"6001002027",
"6001002018",
"6001002024",
"6001002016",
"6001002021",
"6001002015",
"6001002003",
"6001002020",
"6001002025",
"6001002029",
"6001002028",
"6001002022",
"6001005008"]
TotalCompany=0

for Area in CMDtqdm(AreaLi):
    req=s.get("https://www.104.com.tw/cust/list/ajax/index?page=0&area="+Area+"&order=1&mode=s&jobsource=checkc", timeout=100)
    req.encoding = 'UTF-8'
    JsonStr=req.text
    Json = json.loads(JsonStr)
    #取得該地區的總頁數
    totalpage=Json['data']['totalPage']
    
  
    #訪問該地區的所有頁數
    for page in range(1,int(totalpage)):
        ComDatareq = s.get("https://www.104.com.tw/cust/list/ajax/index?page="+str(page)+"&area="+Area+"&order=1&mode=s&jobsource=checkc", timeout=100)
        ComDatareq.encoding = 'UTF-8'
        Company_JsonStr=ComDatareq.text
        Company_jsonLi.append(json.loads(Company_JsonStr))
        

num=0
for Company_json in Company_jsonLi:
    for ele in Company_json['data']['list']:
        num+=1
        #print (num,cusBaseUrl+ele['custUrl'].split("c/")[1])
# In[3]:

download_dir = "Export_104.csv"

csv = codecs.open(download_dir, "w+",'utf_8_sig') 

#定義CSV資料欄位
columnTitleRow = "公司名稱,產業別, 產業說明, 員工人數, 資本額, 聯絡人, 地址, 電話, 傳真, 公司網址, 公司簡介, 商品與服務\n"
csv.write(columnTitleRow)
csv.close()

NowPage=0
for Company_json in CMDtqdm(Company_jsonLi): 
    NowPage+=1
    for ele in CMDtqdm(Company_json['data']['list']):
        try:
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
            
            Custom_reqUrl=cusBaseUrl+ele['custUrl'].split("c/")[1]
            
            CustomDetail=s.get(Custom_reqUrl, timeout=100)
            CustomDetail.encoding = 'UTF-8'


            soup = BeautifulSoup(CustomDetail.text, 'html.parser')
            公司名稱=soup.find_all('h1')[0].text

            while "104人力銀行" in 公司名稱:
                CustomDetail=s.get(Custom_reqUrl, timeout=100)
                CustomDetail.encoding = 'UTF-8'


                soup = BeautifulSoup(CustomDetail.text, 'html.parser')
                公司名稱=soup.find_all('h1')[0].text
                time.sleep(2)


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




            TotalCompany+=1

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
            #print (NowPage,TotalCompany,公司名稱)
            row=row.replace("\n","").replace("\r","")
            try:
                csv = codecs.open(download_dir, "a+",'utf_8_sig') 
                csv.write(row.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
                csv.write("\n")
                csv.close()
            except:
                csv.close()
                pass
        except:
            pass
       
csv.close()
