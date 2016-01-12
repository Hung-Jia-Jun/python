import requests
import urllib.request
import urllib.parse
values = {
'txtAccount':'XXXXXXXXXXXXXX',
'txtPwd':'xxxxxxxxxxxxxxxxxxxxx'
}
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'37',
'Content-Type':'application/x-www-form-urlencoded',
'Cookie':'ASP.NET_SessionId=ikodrljjvqhzvba5wqdhljfv',
'Host':'140.129.253.29',
'Origin':'http://140.129.253.29',
'Referer':'http://140.129.253.29/Usc/HomePage/flogin.aspx',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

data = urllib.parse.urlencode(values)
#req = urllib.request.Request('http://140.129.253.29/Usc/HomePage/flogin.aspx', data=data)
#res=requests.post("http://140.129.253.29/personal/pstudent/CheckID.aspx", data=payload)
res2=requests.post("http://140.129.253.29/Usc/HomePage/flogin.aspx",data=data,headers=headers)
res2.text
