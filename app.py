#coding:utf-8
import jieba
jieba.set_dictionary('dict.txt')
with open('stops.txt', 'r', encoding='utf8') as f:
  stops=f.read().split('\n')
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
def processingMssage(mes):
    test=''
    mes_=[]
    words = jieba.cut(mes)
    for word in words:
       if word not in stops:
          test +=word+' '
          mes_.append(word)
    #test=searchQuestion(mes_)
    #checkenable(mes_)
    cal_index(2)
    return test
def searchQuestion(mes_cut):
#output answer
    pro_qna_list=[]
    with open('processed.csv', 'r') as pro_qna:
        for line in pro_qna.readlines():
            pro_qna_cut=line.strip()
            pro_qna_list.append(pro_qna_cut.split(','))

    finalIndex=[]
    addweight=[0.5,1,3,1.5,1.5,1.5]
    enable=checkenable()
    for i in range(len(enable)):
      findIndex= cal_index(i)
      if findIndex:
        if finalIndex:
          #print(i,findIndex)
          findIndex=[findIndex[j]*addweight[i] for j in range(len(findIndex))]
          finalIndex=[finalIndex[j]+findIndex[j] for j in range(len(finalIndex))]
        else:
          #print(i,findIndex)
          finalIndex=([findIndex[j]*addweight[i] for j in range(len(findIndex))])

    #print('fin',finalIndex)
    maxindex=finalIndex.index(max(finalIndex))
    #print(maxindex,finalIndex[maxindex] )

    #+1是因為 processing有欄位名稱
    #print(pro_qna_list[maxindex+1][0],pro_qna_list[maxindex+1][1])
    return pro_qna_list[maxindex+1][1]

def checkenable(mes):
  enable=[0,0,0,0,0,0]
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
  return enable
def cal_index(i):
  r_list=[]
  findIndex=[]
  term_id=0   
 

  if enable[i]==1:
    with open('w'+str(i+1)+'.csv', 'r') as r:
      for line in r.readlines():
        r_cut=line.strip()
        if r_cut=='':
          r_cut='error'
        r_list.append(r_cut.split(','))

      terms=[]
      for term in r_list: 
        terms.append(term[1].split())
      for term in terms:
        count=0
        for t in term:
          for word in mes:
            if t==word:
              count+=1
              #print(t,word)
        findIndex.append(count)
        term_id+=1 
  return findIndex
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
           +'天氣狀"{}'.format(status["alt"])+'\n'\
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
