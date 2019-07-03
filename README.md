可以參考一下步驟一一實踐 [問答linebot],謝謝

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

* Step1. 先制定QnA題目，在此我是選擇台灣的公開資料集來充當。
![]( https://github.com/HsinTieh/linebot-for-QnA/blob/master/img/dataset.png) 
資料集的形式⇧。

* Step2. 將資料集作處理(斷詞後依字數拆分檔案)
>此步驟相關內容在 processingdataV2.ipynb 的檔案裡
   
* Step3. Heroku 設定
 > 3.1依據下面網址制定heroku與linebot<br>
```https://yaoandy107.github.io/line-bot-tutorial/```

 > 3.2 修改requirements.txt
 >內容請自requirements.txt 查看

 > 3.3 將從processingdataV2.ipynb下載的檔案移置heroku所在的資料夾，然後PUSH上去
 ![](https://github.com/HsinTieh/linebot-for-QnA/blob/master/img/move.png)

* Step4. 修改app.py
  >內容請自 app.py查看

    
 ### ★★★ 要更新linebot一定要重新PUSH到heroku ★★★

* Step5. 結果呈現
>以下表格為資料集隨機擷取出的幾個問題，Question為原始問題，test Q為從Question修改後我們實際要測試的問題，Answer為答案。
<table>
    <tr>
        <td>Question</td>
        <td>test Q</td>
        <td>Answer</td>
    </tr>
     <tr>
        <td>可於哪裡查詢到房屋是否為海砂屋?	</td>
        <td>請問哪裡可以知道房屋為海砂屋</td>
        <td>臺北市建築管理工程處使用科</td>
    </tr>
     <tr>
        <td>旅客可以在車站出入口散發傳單、宣傳品嗎？</td>
        <td>旅客能在車站附近散發傳單或是宣傳品嗎</td>
        <td>臺北大眾捷運股份有限公司</td>
    </tr>
     <tr>
        <td>孕婦罹患德國麻疹會不會生下畸形兒？</td>
        <td>孕婦得到德國麻疹有可能會懷上畸形兒</td>     
        <td>臺北市政府衛生局疾病管制科</td>
    </tr>
      <tr>
        <td>海芋季活動今年有為行動不便的市民朋友準備幾項措施，讓他們也可安心上山賞花？</td>
        <td>海芋季活動今年有什麼設施為行動不變的民眾提供?</td>   
        <td>臺北市政府產業發展局農業發展科</td>
    </tr>
      <tr>
        <td>智慧停車路段無實體單據，但公司行號要實體單據繳費，該如何處理?</td>
        <td>智慧停車路段沒有實際單據，該如何處理?</td>
        <td>臺北市政府資訊局應用服務組</td>
    </tr>
</table>


## **Linebot 測試結果**
![](https://github.com/HsinTieh/linebot-for-QnA/blob/master/img/lineshow.png)

### :::補充:::
>如果出現問題但卻不知道怎麼解決，可以用下列指令即時除錯。<br>
```heroku logs --tail --app herokuAppName```
 
