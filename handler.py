# handler.py

'''
引用庫
'''
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage, QuickReply, QuickReplyButton, TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
import configparser
from utils_ import save_img
from predict import predict_food_content
from line_templates import food_nutrition_fact

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
        bubble = food_nutrition_fact()
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("flex", bubble)
            )

