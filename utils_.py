
# utils_.py
'''
引用庫
'''
from pathlib import Path
import os

'''
變數區
'''
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

# def show_img():
#     '''
#     顯示模型標註圖片
#     '''
#     confirm_template = ConfirmTemplate(
#                             text='請問結果是否正確?',
#                             actions=[
#                                 MessageAction(label='是', text='是'),
#                                 MessageAction(label='否', text='否')
#                             ]
#                         )
#     return confirm_template


# def delete_img(self, img_path):
#     '''
#     刪除圖片
#     '''
#     if os.path.isfile(img_path):
#         os.remove(img_path)
#         print("delete success")