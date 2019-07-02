import zeep
import json
wsdl = 'http://60.248.91.143/services/nahooWebservice?WSDL'
client = zeep.Client(wsdl=wsdl)
shopInfo = client.service.shopInfo('10')
shopInfo = json.loads(shopInfo)
print(shopInfo)