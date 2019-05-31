#coding:utf-8
import requests
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('gqrWH56NN40DOghtI4btCvZoNv6h6GcGp4XAKF6L71emwFCVrrfE3tuWAZzdCWf9gnCUHWD7wDx0YS/YwdI5wtAqbNJoPReavwCrWQUtJXT2x17Qp8JkodcXfi2qFWbsYYS1shKXa0ozfkO6OMoRUAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4117754dd6e1af39e1fdc37749aed80b')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
     message = TextSendMessage(text=weather_fun(event.message.text))
     line_bot_api.reply_message(event.reply_token, message)

def weather_fun(message):
    city=city_fun(message)

    return city
def city_fun(sentence):
    if "高雄" in sentence:
        return 'Kaohsiung_City'
    elif "台北" in sentence:
        return 'Taipei_City'    
    elif "台中" in sentence:
        return 'Taichung_City'
    elif "天氣" in sentence:
         return 'Taichung_City'
    return sentence
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
