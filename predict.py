# predict.py

'''
引用庫
'''
import configparser
from pathlib import Path
import torch
import os
import cv2
import requests
import numpy as np
import time
import shutil
from PIL import Image
import json
from json import load

'''
變數區
'''
file_path = Path(__file__).resolve().parent

model_path = os.path.join(file_path, "static/model/best.pt") # 指定訓練好的模型位置
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path) # 載入訓練好的模型

# save_img_path = os.path.join(file_path, "static/imgs") # 預測圖片儲存位置

food_calorie_path = os.path.join(file_path, "static/json/food_calorie")

'''
函式區
'''
def predict_food_content(filename):
    '''
    食物組成判斷
    :param filename : 想要預測的圖片檔名
    return 食物組成以及熱量，將所有資訊包成json格式
    '''
    # 讀取圖片
    img = cv2.imread(f"{file_path}\static\imgs\{filename}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 模型預測
    results = model(img)
    result_df = results.pandas().xyxy[0]
    # 預測結果儲存
    results.save()
    
    # 載入食物熱量表
    food_calorie = load(
        open(os.path.join(food_calorie_path, "food_calorie.json"), "r", encoding="utf-8")
        )
    # 計算熱量
    result_df['fat'] = result_df['name'].map(food_calorie)
    content = list()
    for i in range(len(result_df)):
        info = dict()
        info["food"] = result_df['name'][i]
        info["fat"] = f"{(result_df['fat'][i])} kcals"
        content.append(info)
    contents = json.dumps(content)
    # 將食物組成以及熱量資訊包成json
    with open(os.path.join(file_path, "static/json/predict_result/predict.json"), "w") as file:
        file.write(contents)
    # return contents
 
    