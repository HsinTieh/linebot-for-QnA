import jieba
import pandas as pd 
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
    message = TextSendMessage(text=processingMssage(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)
#將句子斷詞
def processingMssage(mes):
    with open('stops.txt', 'r', encoding='utf8') as f:
        stops=f.read().split('\n')
    splitedStr=''
    words = jieba.cut(mes)
    mes_cut=[]
    for word in words:
      if word not in stops:
        splitedStr+=word+' '
        mes_cut.append(word)
    searchQuestion(mes_cut)
    return splitedStr
def searchQuestion(mes):
    #pro_qna=pd.read_csv('processed.csv',header=None,dtype=str)
    #pro_qna.columns=['question','answer']
    #pro_qna=pro_qna[1:]

    enable=[0,0,0,0,0,0]
    print(mes)
    for m in mes:
      if len(m)==1:
        enable[0]=1
      elif len(m)==2:
        enable[1]=1
  
      elif len(m)==3:
        enable[2]=1
  
      elif len(m)==4:
        enable[3]=1
  
      elif len(m)==5:
        enable[4]=1
  
      else :
        enable[5]=1
    return 0

import os
if __name__ == "__main__":

    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)