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

'''
變數區
'''
file_path = Path(__file__).resolve().parent
bubblePath = os.path.join(file_path, "static/json/food_nutrition_fact")

'''
定義
'''
def food_nutrition_fact():
    '''
    將預測結果加入line bubble，並顯示在Flex Message中
    param 
    '''
    bubble = load(
        open(os.path.join(bubblePath, "food_nutrition_fact.json"), "r", encoding="utf-8")
    )

    contents = json.load(
        open(os.path.join(file_path, "static/json/predict_result/predict.json"), "r", encoding="utf-8")
    )

    try:
        if len(contents) > 0:
            line_bubble_contents = list()

            total_calorie = 0

            for info in contents:
                bubble_content = copy.deepcopy(bubble["body"]["contents"][2]["contents"][0])
                bubble_content["contents"][0]["text"] = info["food"]
                bubble_content["contents"][1]["text"] = info["fat"]
                fat = info["fat"]
                food_calorie_patten = re.findall(r'\d+', fat)

                total_calorie += int(food_calorie_patten[0])
                line_bubble_contents.append(bubble_content)

            total_calorie_content = copy.deepcopy(bubble["body"]["contents"][-1]["contents"][2])
            total_calorie_content["contents"][1]["text"] = f"{total_calorie} kcals"

            line_bubble_contents.append(copy.deepcopy(bubble["body"]["contents"][-1]["contents"][1]))
            line_bubble_contents.append(total_calorie_content)
            bubble["body"]["contents"][2]["contents"] = line_bubble_contents
    
    except Exception as e:
        print("An error occurred:", str(e))

    return bubble

# def confirm_template():
#     confirm_template = load(
#         open(os.path.join(bubblePath, "food_nutrition_fact.json"), "r", encoding="utf-8")
#     )
