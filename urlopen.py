import urllib.request
#更新版後urllib2包在python3內了，所以直接呼叫就可以了
res=urllib.request.urlopen('http://macloudlab.com/%E8%AA%8D%E8%AD%98facebook-graph-api/')
res.read()
