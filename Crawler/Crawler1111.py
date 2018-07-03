
# coding: utf-8

# In[ ]:


e


# In[2]:



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

s = requests.Session()
s.headers.update({"Referer":"https://www.104.com.tw/cust/list/index/?page=4&area=6001001009,6001001008&order=1&mode=s&jobsource=checkc",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"})


req=s.get("https://www.1111.com.tw/job-bank/job-index.asp?si=2&ss=s&co=100109&ps=23&pt=1", timeout=100)
req.encoding = 'UTF-8'


# In[ ]:


soup = BeautifulSoup(req.text, 'html.parser')

num=0
for ele in soup.find_all('a'):
    if 'corp/' in ele.get('href'):
        if '#c4' not in ele.get('href'):
            num+=1
            CompanyUrl=' https://'+ele.get('href')[2:]
            print (num,CompanyUrl)
            Detail=s.get(CompanyUrl, timeout=100)
            Detail.encoding = 'UTF-8'
            #find_all("li", {"class": "posR"})

            soup = BeautifulSoup(Detail.text, 'html.parser')
            for ele in soup.find_all("li", {"class": "posR"}):
                print (ele.text)
            
            for ele in soup.find_all("div", {"class": "listContent"}):
                print (ele.text)
                
         
            pdb.set_trace()
print (" ")


# In[ ]:


selector = etree.HTML(Detail.text)
         divs = selector.xpath('//*[@id="c1"]/div[1]/article[1]/ul/li')
         pdb.set_trace()
         for ele in divs:
             print (ele.div[2])
             ele.SubElement(root, "div")
         divs = selector.xpath('//*[@id="c1"]/div[1]/article[1]/ul/li[2]/div[2]')
         for ele in divs:
             print (ele.text)
         divs2 = selector.xpath('//*[@id="c1"]/div[1]/article[1]/ul/li[3]/div[2]/a')
         for ele in divs2:
             print (ele.text)
             

