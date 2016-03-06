import requests
import urllib2,pdb
from bs4 import BeautifulSoup as bs
import string,random,sys,re
from requests import Request, Session
print u"CSRF token:"
#csrfToken = raw_input().decode(sys.stdin.encoding)
print u"KKtixToken:"
#kktixToken=raw_input().decode(sys.stdin.encoding)
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def  GenPassword(length):

    numOfNum =  random.randint( 1 ,length - 1 )
    numOfLetter =  length -  numOfNum

    slcNum =  [random.choice(string.digits) for  i in  range (numOfNum)]

    slcLetter =  [random.choice(string.lowercase) for  i in  range (numOfLetter)]

    slcChar =  slcNum +  slcLetter
    random.shuffle(slcChar)

    genPwd =  ''.join([i for  i in  slcChar])
    return  genPwd
GetCookie={
    "__asc":"5cdcafe71534c730a0218ce20e4",
    "__auc":"5cdcafe71534c730a0218ce20e4",
    "_ga":"GA1.2.308046586.1457276521",
    "kktix_session_token_v2":"ae5d054a7f3b4f3523b1384ace7bfb57",
    "X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2",
}
my_referer='https://kktix.com/events/chaiparty-0401/registrations/new'
header={
"Host":"queue.kktix.com",
"Content-Length": "468",
"Origin":"https://kktix.com",
"User-Agent":"Mozilla/5.0(Linux; X11)",
"Content-Type":"text/plain",
"Cookie": "__asc:5cdcafe71534c730a0218ce20e4,__auc:5cdcafe71534c730a0218ce20e4,_ga:GA1.2.308046586.1457276521,kktix_session_token_v2:ae5d054a7f3b4f3523b1384ace7bfb57,X-DevTools-Emulate-Network-Conditions-Client-Id:43940E8F-A956-427B-9532-C7AC34BB6BB2",
'Referer':"https://kktix.com/events/chaiparty-0401/registrations/new",
"X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2",
"DNT ": "1"

}
datas={
    "tickets":
    {
        "id":48732,
        "quantity":4,
        "invitationCodes":"[]",
        "agreeTerm":"true",
        "member_code": "",
        "use_qualification_id":"null"
    }

}
csrfToken = '' .join(randomword(86))
res=requests.post("https://queue.kktix.com/queue/scandaltour2016?authenticity_token=67hR9Cv4tyj85lU0rHaMfavHin%2BdwDJRBiLjGjf3xdGT9urmLKAHQGLT63y36cM0Y8eBH0XI8mqh5zV7UfSidw%3D%3D",data=datas,headers=header,cookies=GetCookie)
pdb.set_trace()
print res.text
RequestGet={
    "Connection":"keep-alive",
    "Cookie":GetCookie,
    "DNT":"1",
    "Host":"queue.kktix.com",
    "Origin":"https://kktix.com",
    "X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2",
    "Referer":"https://kktix.com/events/scandaltour2016/registrations/new",
    "Accept-Encoding":"gzip,deflate,sdch",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
}
Xref={"X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2"}
urlreq="https://queue.kktix.com/queue/token/8c94606d-3744-4c80-8e91-d51f68a02e9e"
req = Request('GET', urlreq,data=Xref,headers=RequestGet)
#res2=s.get("https://queue.kktix.com/queue/token/9a3991ba-2477-4cdd-9c23-12a636c7379a",headers=RequestGet)
#print req.text
