# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import codecs
from lxml import etree
import sys
import time
import pdb
from tqdm import tqdm_notebook
from tqdm import tqdm as CMDtqdm
import shutil
import io
import requests
s = requests.Session()
s.headers.update({"Referer":"https://www.104.com.tw/cust/list/index/?page=4&area=6001001009,6001001008&order=1&mode=s&jobsource=checkc",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest","X-DevTools-Emulate-Network-Conditions-Client-Id": "C7D26572671D1ADA8BD2CADB426BBA24"})



AreaLi=["100109",
"100108",
"100226",
"100227",
"100218",
"100224",
"100216",
"100221",
"100215",
"100203",
"100220",
"100225",
"100229",
"100228",
"100222",
"100508"]

download_dir = "Export_1111.csv"
csv = codecs.open(download_dir, "w+",'utf_8_sig') 
#定義CSV資料欄位
columnTitleRow = "公司名稱,產業別, 產業說明, 員工人數, 資本額, 地址, 電話, 傳真, 公司網址, 公司簡介, 商品與服務\n"
csv.write(columnTitleRow)
csv.close()
for Area in CMDtqdm(AreaLi):
    req=s.get("https://www.1111.com.tw/job-bank/job-index.asp?si=2&ss=s&co="+Area+"&ps=10000&pt=1", timeout=100)
    req.encoding = 'UTF-8'
    

   
   


    soup = BeautifulSoup(req.text, 'html.parser')

    ComLen_num=0
    for ele in CMDtqdm(soup.find_all('a')):
        if 'corp/' in ele.get('href'):
            if '#c4' not in ele.get('href'):
                ComLen_num+=1
                CompanyUrl=' https://'+ele.get('href')[2:]
                
                #公司序號
                ComapnyNumber=ele.get('href')[2:].split('corp/')[1].split('/')[0]
                
                
                
                #進入公司詳細資料頁面
                Detail=s.get(CompanyUrl, timeout=100)
                Detail.encoding = 'UTF-8'
                #find_all("li", {"class": "posR"})
                
                #分析公司詳細資料
                soup = BeautifulSoup(Detail.text, 'html.parser')
                
                Detail_Dic={"聯絡地址":"地址",
                            "行業別":"產業別",
                            "行業說明":"產業說明",
                            "資本額":"資本額",
                            "員工人數":"員工人數",
                            "公司電話":"電話",
                            "公司傳真":"傳真",
                            "網站位址":"公司網址",
                            "公司簡介":"公司簡介",
                            "商品與服務":"商品與服務"}
                公司名稱=''
                產業別=''
                產業說明=''
                員工人數=''
                資本額=''
                地址=''
                電話=''
                傳真=''
                公司網址=''
                公司簡介=''
                商品與服務=''
                
                #做資料定位用
                MapLi=["公司名稱",
                "產業別",
                "產業說明",
                "員工人數",
                "資本額",
                "地址",
                "電話",
                "傳真",
                "公司網址",
                "公司簡介",
                "商品與服務"]
                
                #定位到結果的空輸入欄位
                ResultMapLi=[	"",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                ""]
                #公司名稱
                for ele in soup.find_all("li", {"class": "posR"}):
                    if ele.text.replace(" ","") != "":
                        公司名稱=ele.text
                
                #print (ComLen_num,公司名稱,CompanyUrl)
                
                公司簡介=soup.find_all("p", {"class": "datainfo boxsize"})[0].text
               
                
                selector = etree.HTML(Detail.text)
                divs = selector.xpath('//*[@id="c2"]/div/div/article/div[1]/div[1]/div[1]/p/text()')
                row=""
                for ele in divs:
                    商品與服務+=ele
                
                
                
                num=0
                #公司詳細資料，資本額 員工數....等
                for ele in soup.find_all("div", {"class": "listTitle"}):
                    num+=1
                    Datatype=ele.text.replace('：',"")
                    
                    #定位資料位置
                    Pos_num=0
                    for DataMapLo in MapLi:
                        if Detail_Dic.get(Datatype)!=None:
                            if DataMapLo==Detail_Dic.get(Datatype):
                                break
                        Pos_num+=1
                    #填入到相應的位置
                    ResultMapLi[Pos_num-1]=soup.find_all("div", {"class": "listContent"})[num-1].text.replace('\xa0','')
                
                
                ResultMapLi[-3]=公司簡介
                ResultMapLi[-2]=商品與服務
       
                
                ResultMapLi.insert(0, 公司名稱)
                columnRow=''
                for ele in ResultMapLi:
                    columnRow+=ele.replace(",","")+','
                        
                csv = codecs.open(download_dir, "a+",'utf_8_sig') 
                columnRow=columnRow.replace("\n","").replace("\r","")
                try:
                    csv.write(columnRow.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
                    csv.write('\n')
                    csv.close()
                except:
                    pdb.set_trace()
                    csv.close()
                
                #公司聯絡方式列表  因為list pop 是從尾開始取出  也呼應公司資料是電話TEL先，所以取出後輪尋下一個FOX
                CompanyData=['FOX','TEL']
                #下載公司電話與傳真圖片
                for ele in soup.find_all("img"):
                    
                    #依據圖片網址都擁有  graphHandle  的特徵  只要在列表裡面找到這個特徵就抓取下來
                    if 'graphHandle' in ele.get('src'):
                        
                        #重新構造圖片下載網址進行下載
                        ImgUrl='https://www.1111.com.tw'+ele.get('src')
                        
                        #使用requests 進行下載圖片
                        response = requests.get(ImgUrl, stream=True)
                        
                        #公司聯絡資料類別
                        CompanyData_Type=CompanyData.pop()
                        #寫入圖片檔儲存起來
                        with io.open(CompanyData_Type+'\\'+ComapnyNumber+"_"+CompanyData_Type+'.png', 'wb') as file:
                            file.write(response.content)
                        


