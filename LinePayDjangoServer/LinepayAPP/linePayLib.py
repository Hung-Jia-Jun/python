import requests
import json
import pdb
import uuid
class linePay:
    def __init__(self):
        self.baseUrl = 'https://sandbox-api-pay.line.me/v2/payments'
        self.channelId,self.channelSecret = self.readLinePayID()
    
        self.headers = {'Content-Type': 'application/json',
                    'X-LINE-ChannelId':self.channelId,
                    'X-LINE-ChannelSecret':self.channelSecret}
        self.reserveUrl = self.baseUrl + '/request'
    def reserveOrder(self,productName,amount):
        self.productName = productName
        self.amount = amount
        self.orderId = uuid.uuid4().hex
        data ={'productName':productName,
                'productImageUrl':"https://imgur.com/gallery/NaGrZUz",
                'amount':self.amount,
                'currency':"TWD",
                'confirmUrl':'http://28e71751.ngrok.io/confirm?orderId='+self.orderId,
                'orderId':self.orderId}
                        
        self.paymentResponse = requests.post(self.reserveUrl, headers=self.headers, json=data)
        
        self.getPaymentURL()

    def getPaymentURL(self):
        _paymentJson = json.loads(self.paymentResponse.text)
        self.paymentURL = _paymentJson['info']['paymentUrl']['web']
        self.transactionId = _paymentJson['info']['transactionId']

    def readLinePayID(self):
        f = open("LinePayID.txt")
        lines = f.readlines()
        _channelId = lines[0].split('ChannelId=')[1].replace("\n","")
        _channelSecret = lines[1].split('ChannelSecret=')[1].replace("\n","")
        f.close()
        return _channelId,_channelSecret
if __name__ == '__main__':
    linePay = linePay()

    productName = 'Test123'
    amount = '1000'

    linePay.reserveOrder(productName,amount)
    
    print(linePay.paymentURL)
    print(linePay.transactionId)
