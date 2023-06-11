# health_management_line_bot

## 專案結構

.  
├── readme.md   
├── app.py    
├── handlers.py   
├── line_templates.py  
├── utils.py  
├── predict.py   
├── Static     
│   ├── model  
│   ├── imgs  
│   └── json  
└── config.ini

- `readme.md`：應用程式的說明文件，包括如何安裝、配置和運行應用程式。
- `app.py`： Flask 主要程式。
- `handler.py`：設定 Webhook、設定 Handler 等，用於處理收到的訊息，並回應相應的內容。
- `line_templates.py`：包含 Line Bot 所使用的樣板訊息。
- `utils.py`：包含一些輔助函式。
- `predict.py`： 載入模型進行預測。
- `Static/`：包含靜態資源。
- `config.ini`：包含 Line bot 必要參數。



## 如何使用

1. 從github下載此專案。
2. 執行app.py 
3. 執行ngrok http 8080

## 相關連結

- [Line Developers](https://developers.line.biz/en/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [LineBot SDK](https://github.com/line/line-bot-sdk-python)
