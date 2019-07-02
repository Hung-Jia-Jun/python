#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LinepayAPP.settings")

from django.shortcuts import render
from django.http import HttpResponse
from linebot import LineBotApi
from linebot.exceptions import *
from django.views.decorators.csrf import csrf_exempt
from linebot import *
import pdb
#from linebot.models import *
from LinepayAPP.classLib import *
#from LinepayAPP.models import clientSession

line_bot_api = LineBotApi('XNE8bmST6IvwcucMwcc04BpW1Elj5PfdrO4c3LWHck+6/ajJj3GkwsbCHFKf9bZoMdZTpGWLFgHw9ThHNk7iK33xZkR6+QalKa5qOCaqi5JrLa6R8Madhr98iBStVZxnd19+ZbrBhPeZkyQI26xSmgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4cd68a056f75e966b7e05d21fc9990db')

@csrf_exempt
def callback(request):
    messageCallback = request.body
    
    decodeToText = decodeJson(messageCallback)
    lineEvent = decodeToText.parse()
    pdb.set_trace()
    ClientMsg = lineEvent.events[0].message.text
    replyToken = lineEvent.events[0].replyToken

    line_bot_api.reply_message(
        replyToken,
        TextSendMessage(text=ClientMsg))

    return HttpResponse('OK')


#付款狀態確認
def confirm(request):
    transactionId = request.GET["transactionId"]
    orderId = request.GET["orderId"]
    print (transactionId)
    print (orderId)
    return HttpResponse("OK")
