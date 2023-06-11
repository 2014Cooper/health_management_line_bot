
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
    :param img_id : 使用者傳送圖片後，當次訊息所產生的圖片id
    :param img_content : 當次使用者所傳送的圖片訊息內容
    :return 圖片檔名
    '''
    filename = f"{img_id}.jpg" # 使用"img_id"作為圖片名稱
    img_path_name = os.path.join(img_path, filename) # 圖片存取位置
    with open(img_path_name, 'wb') as f:
        for chunk in img_content.iter_content():
            f.write(chunk)
    return filename

def show_predicted_img(img_id):
    '''
    :顯示模型預測後，產生的圖片
    :return 顯示圖片的訊息
    '''
    # 經過模型預測後的圖片，是存在另外產生資料夾，但是flask預設存取靜態資源的資料夾為"static"，因此先將模型預測後的圖片移動到"static"下面
    predict_img_name = "image0.jpg" # 模型預測後的圖片名稱
    original_img_path = os.path.join(file_path, f"runs/detect/exp/{predict_img_name}") # 模型預測後的圖片原始位置
    target_img_path = os.path.join(img_path, f"{img_id}_predict.jpg") # 預測後圖片存到"static/imgs"的位置，並更改圖片名稱
    shutil.move(original_img_path, target_img_path) # 移動圖片
    
    # 顯示圖片的訊息
    predict_img = ImageSendMessage(
        original_content_url = f"{end_point}/static/imgs/{predict_img_name}",
        preview_image_url = f"{end_point}/static/imgs/{predict_img_name}"
    )
    return predict_img


def delete_folder():
    '''
    刪除模型預測後，所產生的資料夾
    '''
    remove_folder = "./runs"
    shutil.rmtree(remove_folder, ignore_errors=True)

    # for filename in os.listdir(img_path):
    #     img_file_path = os.path.join(img_path, filename)
    #     if os.path.isfile(img_file_path):
    #         os.remove(img_file_path)
