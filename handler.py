# handler.py

'''
引用庫
'''
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage, QuickReply, QuickReplyButton, TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
import configparser
from utils_ import save_img,  show_predicted_img, delete_folder
from predict import predict_food_content
from line_templates import food_nutrition_fact, confirm_template

'''
變數區
'''
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}

'''
函式區
'''
@ handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    '''
    處理圖片訊息
    '''
    if isinstance(event.message, ImageMessage):
        img_id = event.message.id
        img_content = line_bot_api.get_message_content(img_id)
        try:
            filename = save_img(img_id, img_content) # 將使用者傳送的圖片儲存
            predict_food_content(filename) # 圖片使用訓練好的模型進行預測
            predict_img_ = show_predicted_img(img_id) # 顯示預測圖片
            bubble = FlexSendMessage("flex", food_nutrition_fact()) # 顯示食物組成
            confirm = confirm_template() # 顯示確認模板，讓使用者確認分析結果是否正確

            # 將預測圖片、食物組成以及確認模板在一次回覆訊息中同時顯示
            reply_arr = []
            reply_arr.append(predict_img_)
            reply_arr.append(bubble)
            reply_arr.append(confirm)
            line_bot_api.reply_message(event.reply_token, reply_arr) # 回覆訊息

            delete_folder() # 刪除模型預測後產生的資料夾
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("機器人壞掉了!"))

        

        

