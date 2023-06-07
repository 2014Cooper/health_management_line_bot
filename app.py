# app.py

'''
引用庫
'''
from handler import handler
import os
# from pathlib import Path
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import Flask, request, abort

'''
變數區
'''
app = Flask(__name__)

'''
主程式
'''
@ app.route("/callback", methods=['POST'])
def callback():
    '''
    處理linebot伺服器回傳data
    '''
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


if __name__ == "__main__":
    app.run(port=8080, debug=True)
