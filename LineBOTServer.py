from flask import Flask, request, abort
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, 
	FollowEvent,
	TextSendMessage,
	ImageSendMessage,
	TemplateSendMessage,
	CarouselTemplate,
	StickerSendMessage,
	ButtonsTemplate,
	PostbackTemplateAction,
	MessageTemplateAction,
	URITemplateAction,
	ImageCarouselTemplate,
	ImageCarouselColumn,
	CarouselColumn,
)
import pdb
app = Flask(__name__)

line_bot_api = LineBotApi('Pk6Wrq32ctiw/gk/7/fPT3/VHXoINfdCk1mLf5OkKygSREGK7M9xuj1AoJImmAye1u42ad+UMUlZOBfoTkvxLmddKFaOf3mrpE6fyp75Wx8d2Q7a18kkWU9oW42sJsDg7lM/MuzX5ic4dztlhtQEjgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f6cc92ff12e1b2bc625b8a2604918117')


@app.route("/", methods=['POST'])
def index():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'

@app.route('/PushMsg/<username>')
def PushMsg(username):
	line_bot_api.multicast(['Ue2a91beba135696d6b7cafad52e51587'], 
	TextSendMessage(text=username))
	return "OK"

def CarouseObj_MessageTemplate(item): #輪播圖子物件  全文字回傳
	
	thumbnail_image_url_=item[0]
	title_=item[1]
	text_=item[2]
	actions_=[]
	for MessageTemplateActionObj in item[3]:
		actions_.append(MessageTemplateAction(
			label=MessageTemplateActionObj[0],
			text=MessageTemplateActionObj[1]))


	CarouselColumnObj=CarouselColumn(
		thumbnail_image_url=thumbnail_image_url_,
		title=title_,
		text=text_,
		actions=actions_,
	)
	return CarouselColumnObj
def CreateCarouselTemplate(items):
	columns_=[]
	for item in items:
		columns_.append(CarouseObj_MessageTemplate(item) )
	Carousel_template=TemplateSendMessage(
	alt_text='Carousel template',
	template=CarouselTemplate(
			#創建輪播圖子物件
			columns=columns_ 
		))
	return Carousel_template


@handler.add(FollowEvent)
def handle_follow(event):
	carousel_template_message = CreateCarouselTemplate([
				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"阿福智慧家 介紹",
					" ",#description1
					[
						["主題選單","主題選單"],
						[" "," "],
					]
				],
			])
	line_bot_api.reply_message(event.reply_token,carousel_template_message)#,TextSendMessage(text=event.message.text))
		
	return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if event.message.text=="班級查詢/報名":
		carousel_template_message = CreateCarouselTemplate([
				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					" ",#description1
					[
						["我想查詢廣論班級","我想查詢廣論班級"],
						["主題選單","主題選單"],
						[" "," "],
					]
				],
			])
	if event.message.text=="我想查詢廣論班級":
		carousel_template_message = CreateCarouselTemplate([
				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"縣市按鈕",#description1
					[
						["台北市","台北市"],
						["新北市","新北市"],
						["主題選單","主題選單"],
					]
				],
			])
	if event.message.text=="台北市":
		carousel_template_message = CreateCarouselTemplate([
				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市中正區","台北市中正區"],
						["台北市大同區","台北市大同區"],
						["主題選單","主題選單"],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市中山區","台北市中山區"],
						["台北市松山區","台北市松山區"],
						["主題選單","主題選單"],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市大安區","台北市大安區"],
						["台北市萬華區","台北市萬華區"],
						["主題選單","主題選單"],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市信義區","台北市信義區"],
						["台北市士林區","台北市士林區"],
						["主題選單","主題選單"],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市北投區","台北市北投區"],
						["台北市內湖區","台北市內湖區"],
						["主題選單","主題選單"],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					"台北市行政區",#description1
					[
						["台北市南港區","台北市南港區"],
						["台北市文山區","台北市文山區"],
						["主題選單","主題選單"],
					]
				],
			])
	if event.message.text=="主題選單":
		carousel_template_message = CreateCarouselTemplate(
			[
				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"法會/活動",
					" ",#description1
					[
						["我想了解法會/活動","我想了解法會/活動"],
						[" "," "],
						[" "," "],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"研討班報名",
					" ",#description1
					[
						["班級查詢/報名","班級查詢/報名"],
						[" "," "],
						[" "," "],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"迴向服務",
					" ",#description1
					[
						["我要迴向","我要迴向"],
						["我想幫忙迴向","我想幫忙迴向"],
						[" "," "],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"意見回饋服務",
					" ",#description1
					[
						["意見回饋服務","意見回饋服務"],
						[" "," "],
						[" "," "],
					]
				],

				["https://www.taiwan.net.tw/resources/images/Attractions/0001095.jpg",
					"無聊時的小品學習",
					" ",#description1
					[
						["我想聽故事","我想聽故事"],
						["我想聽智慧法語","我想聽智慧法語"],
						[" "," "],
					]
				],
			]
		)
	line_bot_api.reply_message(event.reply_token,carousel_template_message)#,TextSendMessage(text=event.message.text))
	profile = line_bot_api.get_profile(str(event.source).split("userId")[1].split('"')[2])
	print(profile.display_name)
	print(profile.user_id)

if __name__ == "__main__":
	app.debug = True
	app.run(host='127.0.0.1', port= 5000)
