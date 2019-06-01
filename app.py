import jieba
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
jieba.set_dictionary('dict.txt')
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('WCkBEAw4dOLVK612SAnwBPjw67MEN/yZa8/eUMWIoD1J5Rl778sR/83hIoxO74M4qN5jAtC5lQImS4plEVu7qFiu2p9HbZ7EVd2IF9kHSy0h3nutjtHlebraKZgLoA0LFNBp5XRl8TgSg3QqM5wIcQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bd1de79c53f74697cdd7ed769345edc4')

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
    message = TextSendMessage(text=o=processingMssage(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)
def processingMssage(mes):
    with open('stops.txt', 'r', encoding='utf8') as f:
        stops=f.read().split('\n')
    splitedStr=''
    words = jieba.cut(mes)
    for word in words:
      if word not in stops:
       # segments.append({'word':word,'count':1})
        splitedStr +=word+' '
    return splitedStr


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)