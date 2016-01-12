import requests
payload={
'sID':'XXXXXXXXXX',
'sPassword':'XXXXXXXXXXXX',
'btnOk.x':'39',
'btnOk.y':'6'
}
res=requests.post("http://140.129.253.29/personal/pstudent/CheckID.aspx", data=payload)
res.text
