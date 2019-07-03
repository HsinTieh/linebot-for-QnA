"# linebot-for-QnA" 

QnA方式<br>
>[✘] wait.ai <br>
>[✘] QnA Maker<br>
>[✔] Homemade Text mining +excel QA<br>

使用到的東西<br>
>✔ Colab<br>
>✔台北市政府常見問答資料集<br>
```https://www.gov.taipei/News.aspx?n=EEC70A4186D4C828%5C&sms=87415A8B9CE81B16```<br>
>✔Heroku<br>
>✔LineBot<br>
>✔CMD<br>

Step1. 先制定QnA題目，在此我是選擇台灣的公開資料集來充當。
![]( https://github.com/HsinTieh/linebot-for-QnA/blob/master/img/dataset.png) 
資料集的形式⇧。
Step2. 將資料集作處理(斷詞後依字數拆分檔案)
 
 
 
 
 
 

 

 
  
Step3. Heroku 設定
3.1依據下面網址制定heroku與linebot
https://yaoandy107.github.io/line-bot-tutorial/

3.2 修改requirements.txt
 

3.3 將前面下載的檔案移置heroku所在的資料夾，然後PUSH上去
 

Step4. 修改App.py
 
 
   
 

4.5依據將colab撰寫好的程式移到app.py

 
    
4.5 PUSH上去heroku

Step5. 結果呈現
測試QA
Question	Answer
可於哪裡查詢到房屋是否為海砂屋?	臺北市建築管理工程處使用科
旅客可以在車站出入口散發傳單、宣傳品嗎？	臺北大眾捷運股份有限公司
孕婦罹患德國麻疹會不會生下畸形兒？	臺北市政府衛生局疾病管制科
智慧停車路段無實體單據，但公司行號要實體單據繳費，該如何處理?	臺北市政府資訊局應用服務組
海芋季活動今年有為行動不便的市民朋友準備幾項措施，讓他們也可安心上山賞花？	臺北市政府產業發展局農業發展科

結果
 

:::補充:::
如果出現問題但卻不知道怎麼解決，可以用下列指令即時除錯。
heroku logs --tail --app qnaforlinebot
 
