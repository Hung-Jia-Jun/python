import urllib.request#更新版後urllib2包在python3內了，所以直接呼叫就可以了
value={}
value['username']='F1021365'
value['password']='Sai12boat3'
data =urllib.parse.urlencode(value)
url = 'http://140.129.253.29/personal/pstudent/login.aspx'
res=urllib.request.urlopen(url)
geturl=url+"?"+data
res=urllib.request.urlopen(geturl)
res.read()
