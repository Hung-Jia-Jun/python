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

line_bot_api = LineBotApi("Line機器人API")
handler = WebhookHandler('WebHookkey')

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
