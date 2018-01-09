# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : python 3 , 答题闯关辅助，截屏 ，OCR 识别，百度搜索

import io
import urllib.parse
import webbrowser
import requests
import base64
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import  sys
import datetime

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')


def main():
    pull_screenshot()
    img = Image.open("./screenshot.png")

    # 用 matplot 查看测试分辨率，切割

    region = img.crop((50, 350, 1000, 1200)) # 坚果 pro1
    #region = img.crop((75, 315, 1167, 789)) # iPhone 7P

    #im = plt.imshow(img, animated=True)
    #im2 = plt.imshow(region, animated=True)
    #plt.show()

    # 百度OCR API
    api_key = 'vkSrxs5BBia60i9LzAdyzINP'
    api_secret = 'ReugNU3rlLd2PXBUHuxTcKqf2TqV1GsU'


    # 获取token
    host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
    headers = {
        'Content-Type':'application/json;charset=UTF-8'
    }

    res = requests.get(url=host,headers=headers).json()
    token = res['access_token']


    imgByteArr = io.BytesIO()
    #region.save('xxx.png')
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                  params={'access_token': token}, data={'image': base64_data})
    result = ''
    last_qustion_result=''
    last_answer_result=''
    jsonResult=r.json()['words_result']
    resultLen=len(jsonResult)
    qustion_result=jsonResult[0:resultLen-3]
    for i in qustion_result:
        last_qustion_result+=i['words']
    last_qustion_result_array=last_qustion_result.split(".", 1)
    if last_qustion_result_array[0].isdigit():
        result = last_qustion_result_array[1]
    else:
        result=last_qustion_result
    print("问题为:{}".format(result))
    answer_result=jsonResult[resultLen-3:resultLen]
    for i in answer_result:
        last_answer_result=last_answer_result+i['words']+","
    print("答案为:{}".format(last_answer_result))

    query_str=result+" "+last_answer_result
    print("问题问题：{}".format(query_str))
    query_str = urllib.parse.quote(query_str)
    webbrowser.open('https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&word='+query_str)
    #webbrowser.open('https://iask.sina.com.cn/search?searchWord='+query_str)


if __name__ == '__main__':
    now = datetime.datetime.now()
    print("开始搜索：{}".format(now.strftime('%Y-%m-%d %H:%M:%S')))
    main()
    end = datetime.datetime.now()
    print("搜索结束：{}".format(end.strftime('%Y-%m-%d %H:%M:%S')))