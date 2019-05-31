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
line_bot_api = LineBotApi('aX5A4FOUbqrObNFiFGrCjSnNelVTyGKeedWiigHGMSKYUFNoTkod+nzMjtf+6SWFYdfQgBdVals6SxKushKNFBXkISVmdCknqVBGoQPD9Jkqi2jyZqXB0EOLFEU979fST6zQNPpbrZKUfJL71eJJPQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('1bd79676da81086ed9af529e27d517cd')

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
    target_url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/'+city+'.htm'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'unicode' 
    soup = BeautifulSoup(res.text,'html.parser', from_encoding="gb18030")
    head = soup.find('table').thead.find_all('tr')
    body = soup.find('table').tbody.find_all('tr')

    for row in head :
      mes=row.find_all('th')[0].text+"\n"
 
    for row in body :
      time=row.find_all('th')[0].text
      temp=row.find_all('td')[0].text
      com=row.find_all('td')[2].text
      humi=row.find_all('td')[3].text
      status=row.find_all('td')[1].find('img',alt=True)
      mes =mes+ '{}'.format(time)+"\n"\
           +'天氣狀態"{}'.format(status["alt"])+'\n'\
           +'溫度:{}'.format(temp)+"\n"\
           +'舒適度:{}'.format(com)+"\n"\
           +'濕度:{}'.format(humi)+"\n\n"
    return mes
def city_fun(sentence):
    if "高雄" in sentence:
        return 'Kaohsiung_City'
    elif "台北" in sentence:
        return 'Taipei_City'    
    elif "台中" in sentence:
        return 'Taichung_City'
    elif "天氣" in sentence:
         return 'Taichung_City'
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
