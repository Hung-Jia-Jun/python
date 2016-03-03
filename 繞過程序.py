import requests
import urllib2
from bs4 import BeautifulSoup as bs
import string,random

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

my_referer='https://kktix.com/events/scandaltour2016/registrations/new'
header={

"Host":"queue.kktix.com",
"Content-Length": "468",
"Origin":"https://kktix.com",
"User-Agent":"Mozilla/5.0(Linux; X11)",
"Content-Type":"text/plain",
"DNT ": "1"
}
responseChallenge="03AHJ_VutEur7XqPvgmgdPB9ZNEthwwRC9CJ_XcXdteXTeBQW_"
responseChallenge2="b-IYFNBXPFC_hJIGxPmhhG0f32imXVlxzbHj0TCzNL_0TguXQwdpeXS7k4c-BJCiTmp8h_3PDG6yHLIpdhw37gBXHRy61pat2N43j7RyT8O2cI7Ve_6DZCD9dyMfKksUe-a2aC27Yw40S7YFaYrSm4__thonrZUyDTzXBptVZ2tCvc00a-"
responseChallenge3="-YYfQMyDcCDYQWdAZFpgXAifoI8slJ4hP8EwqC4h9Cj"
responseChallenge_Total=responseChallenge+responseChallenge2+responseChallenge3
datas={
    "tickets":
    {
        "id":48732,
        "quantity":4,
        "invitationCodes":"[]",
        "agreeTerm":"true",
        "responseField":"185",
        "responseChallenge":"03AHJ_VuuYvWLlcvdRnVG-qfLlJX0Vr4S4DW2e0f0kv5Y4VqKXA4-c5JG3HCN17So9htpvTMx-gnLKjBW0dhb16hoq6p7A4KmySrzz01Zdei4IP-ObfpPBZrvuxI7V1WX1PE4yGVbVr6hZw24FWA34-1Qa1S2agdys_J7lED91VRfy4v8gj8WuiM-a1HVxtDJTR9LN7dqLGBEiCo9hGHbpwsG5fMjlMK4gcyNwWDGPbXjDx23bJI-OjlYm295LEOlM9CIEqETVjExD"
    }

}
#csrfToken = '' .join(randomword(86))
csrfToken="aD+yE/2yiQ4yT5ylilmk9xfBWtdXiE577Bmt75jAWQRUbdFwkFjASdvu5H7lQh30gOlC090TU/kFjwvtH8O6fw%3D%3D"
cookie={
    "Cookie":"__uvt=; uvts=4EmHI70l7SqXHrG8; _ga=GA1.2.1667600123.1456760657; kktix_session_token_v2=e63dbf705590111d8b88733995ea7fc0; __asc=a6d7fad5153390700092508699f; __auc=a8c767e31532db2ff6580c26a55"
}
s=requests.Session()
s.headers.update({'Referer':my_referer })
res=s.post("https://queue.kktix.com/queue/scandaltour2016?authenticity_token=aD%2ByE%2F2yiQ4yT5ylilmk9xfBWtdXiE577Bmt75jAWQRUbdFwkFjASdvu5H7lQh30gOlC090TU%2FkFjwvtH8O6fw%3D%3D",data=datas,headers=header,cookies=cookie)
#res2=requests.get("https://kktix.com/g/events/2016depapepe/base_info")
print res.text
print res.url
Random8word=GenPassword(8)
Random4word_0=GenPassword(4)
Random4word_1=GenPassword(4)
Random4word_2=GenPassword(4)
Random12word=GenPassword(12)
#res2=s.get("https://queue.kktix.com/queue/token/"+Random8word+'-'+Random4word_0+'-'+Random4word_1+'-'+Random4word_2+'-'+Random12word,headers=header,cookies=cookie)
#print res2.url
