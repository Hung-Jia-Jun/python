import requests
import urllib2
from bs4 import BeautifulSoup as bs
import string,random

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

header={

"Host":"queue.kktix.com",
"Content-Length": "494",
"Origin":"https://kktix.com",
"User-Agent":"Mozilla/5.0(Linux; X11)",
"Content-Type":"text/plain",

}
datas={
    "tickets":
    {
        "id":48732,
        "quantity":1,
        "invitationCodes":"[]",
        "agreeTerm":"true"
    }

}
csrfToken = '' .join(randomword(86))
cookie={
    "Cookie":"__uvt=; uvts=4FBd3YoqsVkbWzTE; _ga=GA1.3.1471822020.1456835505; kktix_session_token_v2=3ca77d7af43e932f4d685e828e420591; __asc=232c8e0415337a927bb1e97b5f4; __auc=e994b26615332383a52f744d6b1"
}
my_referer='https://kktix.com/events/scandaltour2016/registrations/new'
s=requests.Session()
s.headers.update({'Referer':my_referer })
res=s.post("https://queue.kktix.com/queue/scandaltour2016?authenticity_token="+csrfToken,data=datas,headers=header,cookies=cookie)
print res
