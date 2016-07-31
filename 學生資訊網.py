import requests
from bs4 import BeautifulSoup as bs
s=requests.Session()
data={
    "sID":"XXXXXX",
    "sPassword":"XXXXXX",
}
res=s.post("http://140.129.253.29/personal/pstudent/CheckID.aspx?urF1021352",data=data)
print res.text
