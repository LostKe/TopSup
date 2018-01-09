#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 17:31
# @Author  : zsq
# @Site    : 
# @File    : GetTitleBaidu2.py
# @Software: PyCharm
# @desc    :

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

    region = img.crop((50, 350, 1000, 560)) # 坚果 pro1
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
    for i in r.json()['words_result']:
        result += i['words']
    result_array = result.split(".", 1)
    if result_array[0].isdigit():
        result = result_array[1]
    print("获取到问题：{}".format(result))
    result = urllib.parse.quote(result)
    webbrowser.open('https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&word='+result)
    #webbrowser.open('https://iask.sina.com.cn/search?searchWord='+result)


if __name__ == '__main__':
    now = datetime.datetime.now()
    print("开始搜索：{}".format(now.strftime('%Y-%m-%d %H:%M:%S')))
    main()
    end = datetime.datetime.now()
    print("搜索结束：{}".format(end.strftime('%Y-%m-%d %H:%M:%S')))