import requests
payload={
'sID':'F1021365',
'sPassword':'Sai12boat3',
'btnOk.x':'39',
'btnOk.y':'6'
}
res=requests.post("http://140.129.253.29/personal/pstudent/CheckID.aspx", data=payload)
res.text
