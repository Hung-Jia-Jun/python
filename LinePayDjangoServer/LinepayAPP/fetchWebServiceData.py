import zeep
import json
wsdl = 'http://XXX.XXX.XXX.X/services/nahooWebservice?WSDL'
client = zeep.Client(wsdl=wsdl)
shopInfo = client.service.shopInfo('10')
shopInfo = json.loads(shopInfo)
print(shopInfo)
