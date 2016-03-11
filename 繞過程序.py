import requests
import urllib2,pdb
from bs4 import BeautifulSoup as bs
import string,random,sys,re
from requests import Request, Session
from  urllib  import  quote 
GetCookie={
    "user_path_v2":"%2Fuser%2F423729",
    "user_time_zone_offset_v2":"28800",
    "user_time_zone_v2":"Asia%2FTaipei",
    "user_display_name_v2":"uniqe1994",
    "user_avatar_url_v2":"https%3A%2F%2Fwww.gravatar.com%2Favatar%2F3dcee6a94126286fba3686c13216d2a5.png"
}
my_referer='https://kktix.com/events/scandaltour2016/registrations/new'
header={"Host":"queue.kktix.com",
        "Content-Length": "468",
        "Origin":"https://kktix.com",
        "User-Agent":"Mozilla/5.0(Linux; X11)",
        "Content-Type":"text/plain",
        "X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2",
        "DNT ": "1"
       }
datas={
    "tickets":
    {
        "id":49346,
        "quantity":4,
        "invitationCodes":"[]",
        "agreeTerm":"true",
        "member_code": "",
        "use_qualification_id":"null"
    }

}
s=requests.Session()
s.headers.update({'Referer':my_referer })
s.cookies.update({ "__asc":"d52bef0315363cd44a3ef2fe8d2"})
s.cookies.update({ "__auc":"d52bef0315363cd44a3ef2fe8d2"})
s.cookies.update({ "_gali":"ticket_48732"})
s.cookies.update({ "kktix_session_token_v2":"cd2e17f68c98f0b9a2a0d9f3ddabc428"})
s.cookies.update({  "_ga":"GA1.2.704770406.1457662111"})
s.cookies.update({  "_dc_gtm_UA-44784359-5":"1"})  
res=s.post("https://queue.kktix.com/queue/scandaltour2016?authenticity_token=OLoLYfNcTvdBZ74ra8pyIPf7fkH3iSfNBSF9u4%2B0DLUnvOYoFUlytZS2RSoZv8CrKvaOsJx3ISdOj1g8Q3%2BlHg%3D%3D",data=datas,headers={"Host":"queue.kktix.com","Content-Length": "468","Origin":"https://kktix.com","User-Agent":"Mozilla/5.0(Linux; X11)","Content-Type":"text/plain","X-DevTools-Emulate-Network-Conditions-Client-Id":"43940E8F-A956-427B-9532-C7AC34BB6BB2","DNT ": "1"})
#print resCookies




elestr=str(res.text)
elestr2=elestr.split(':')[1]
elestr3=elestr2[1:37]
#print elestr3

d=requests.Session()
d.headers.update({'Referer':"https://kktix.com/events/scandaltour2016/registrations/new" })
d.cookies.update({ "__asc":"d52bef0315363cd44a3ef2fe8d2"})
d.cookies.update({ "__auc":"d52bef0315363cd44a3ef2fe8d2"})
d.cookies.update({ "_gali":"ticket_48732"})
d.cookies.update({ "kktix_session_token_v2":"cd2e17f68c98f0b9a2a0d9f3ddabc428"})
d.cookies.update({  "_ga":"GA1.2.704770406.1457662111"})
d.cookies.update({  "_dc_gtm_UA-44784359-5":"1"})  
print d.cookies.get_dict()
#resurl=d.get("https://queue.kktix.com/queue/token/"+elestr3)
resurl=d.get("data:text/plain;base64,eyJ0b2tlbiI6IjRmYWI5MDJlLWVhYWQtNDcwYS1iZDdiLTc4NzBkODNkNjcxMSJ9")
#print resurl.request.headers
print resurl.url
print resurl.text
