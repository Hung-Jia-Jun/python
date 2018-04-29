from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, 
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print (event.message.text)
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackTemplateAction(
                        label='postback1',
                        text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message1',
                        text='message text1'
                    ),
                    URITemplateAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackTemplateAction(
                        label='postback2',
                        text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageTemplateAction(
                        label='message2',
                        text='message text2'
                    ),
                    URITemplateAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)

    line_bot_api.reply_message(event.reply_token,carousel_template_message)#,TextSendMessage(text=event.message.text))
    profile = line_bot_api.get_profile(str(event.source).split("userId")[1].split('"')[2])
    print(profile.display_name)
    print(profile.user_id)

if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port= 5000)
