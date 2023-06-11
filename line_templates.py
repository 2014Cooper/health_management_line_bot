# line_templates.py

'''
引用庫
'''
from pathlib import Path
import os
import json
from json import load
from predict import predict_food_content
import copy
import re
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage, QuickReply, QuickReplyButton, TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent, ConfirmTemplate, MessageAction)

'''
變數區
'''
file_path = Path(__file__).resolve().parent
bubblePath = os.path.join(file_path, "static/json")

'''
定義
'''
def food_nutrition_fact():
    '''
    將預測結果加入line bubble，並顯示在Flex Message中
    return 包含食物營養以及卡路里的bubble
    '''
    # 載入設計好的bubble模板
    bubble = load(
        open(os.path.join(bubblePath, "food_nutrition_fact/food_nutrition_fact.json"), "r", encoding="utf-8")
    )
    # 載入模型預測後，所儲存的食物組成以及卡路里資訊
    contents = json.load(
        open(os.path.join(file_path, "static/json/predict_result/predict.json"), "r", encoding="utf-8")
    )

    try:
        if len(contents) > 0:
            line_bubble_contents = list()

            total_calorie = 0
            # 將預測食物的組成以及熱量加入bubble模板
            for info in contents:
                bubble_content = copy.deepcopy(bubble["body"]["contents"][2]["contents"][0])
                bubble_content["contents"][0]["text"] = info["food"].replace("_", " ").title()
                bubble_content["contents"][1]["text"] = info["fat"]
                fat = info["fat"]
                food_calorie_patten = re.findall(r'\d+', fat)
                total_calorie += int(food_calorie_patten[0]) # 計算總卡路里
                line_bubble_contents.append(bubble_content)
            total_calorie_content = copy.deepcopy(bubble["body"]["contents"][-1]["contents"][2])
            total_calorie_content["contents"][1]["text"] = f"{total_calorie} kcals" # 將總卡路里加入bubble
            line_bubble_contents.append(copy.deepcopy(bubble["body"]["contents"][-1]["contents"][1]))
            line_bubble_contents.append(total_calorie_content)
            bubble["body"]["contents"][2]["contents"] = line_bubble_contents
    
    except Exception as e:
        print("An error occurred:", str(e))

    return bubble

def confirm_template():
    '''
    新增確認模板，詢問使用者分析結果是否正確
    return 確認模板
    '''
    confirm_template = ConfirmTemplate(
            text='請問分析結果是否正確？',
            actions=[
                MessageAction(label='是', text='Yes'),
                MessageAction(label='否', text='No')
            ]
        )

    confirm_template_message = TemplateSendMessage(
        alt_text='確認分析結果',
        template=confirm_template
    )

    return confirm_template_message
