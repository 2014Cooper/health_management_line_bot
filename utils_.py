
# utils_.py
'''
引用庫
'''
from pathlib import Path
import os
import shutil
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage, QuickReply, QuickReplyButton, TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
import configparser

'''
變數區
'''
config = configparser.ConfigParser()
config.read('config.ini')
end_point = config.get('line-bot', "end_point")
file_path = Path(__file__).resolve().parent
img_path = os.path.join(file_path, "static\imgs")

'''
函式區
'''



def save_img(img_id, img_content):
    '''
    將用戶傳的圖片保存到本地server
    :param img_id : line給的圖片id
    :param content : 圖片訊息內容
    :return    檔名 : 時間戳加img_id
    '''
    filename = f"{img_id}.jpg"
    img_path_name = os.path.join(img_path, filename)
    with open(img_path_name, 'wb') as f:
        for chunk in img_content.iter_content():
            f.write(chunk)
    return filename

def show_predicted_img():
    '''
    顯示模型標註圖片
    '''
    predict_img_name = "image0.jpg"
    original_img_folder = os.path.join(file_path, "runs/detect/exp")
    original_img_path = os.path.join(original_img_folder, predict_img_name)
    target_img_path = os.path.join(img_path, predict_img_name)
    shutil.move(original_img_path, target_img_path)
    
    predict_img = ImageSendMessage(
        original_content_url = f"{end_point}/static/imgs/{predict_img_name}",
        preview_image_url = f"{end_point}/static/imgs/{predict_img_name}"
    )
    print(f'path : {end_point}/runs/detect/exp/image0.jpg')
    return predict_img


# def delete_img(self, img_path):
#     '''
#     刪除圖片
#     '''
#     if os.path.isfile(img_path):
#         os.remove(img_path)
#         print("delete success")