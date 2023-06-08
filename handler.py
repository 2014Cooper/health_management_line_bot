# handler.py

'''
引用庫
'''
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage, QuickReply, QuickReplyButton, TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
import configparser
from utils_ import save_img,  show_predicted_img
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

        filename = save_img(img_id, img_content)

        predict_food_content(filename)

        predict_img_ = show_predicted_img()
        bubble = FlexSendMessage("flex", food_nutrition_fact())
        confirm = confirm_template()

        reply_arr = []
        reply_arr.append(predict_img_)
        reply_arr.append(bubble)
        reply_arr.append(confirm)

        line_bot_api.reply_message(event.reply_token, reply_arr)

