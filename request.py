import base64
import json
import os
import random
import time

import requests
from PIL import Image


def getAuth():
    """
    获取百度API的权限
    """

    # client_id 为官网获取的API Key， client_secret 为官网获取的Secret Key
    host = 'https://aip.baidubce.com/oauth/2.0/token' \
           '?grant_type=client_credentials' \
           '&client_id=imggz3EqEBHwS3Hqe7Kx6AEq' \
           '&client_secret=DlfkAyKxN7Hdl3roThN7QVz99ySSQ0Kq'
    response = requests.get(host)
    return response.json()['access_token']


def ocr(filepath, x1, y1, x2, y2):
    img = Image.open(filepath)
    basicpath = "G:/CBIB/medical-record-ocr/pic/tmp/"
    if not os.path.exists(basicpath):
        try:
            os.mkdir(basicpath)
        except:
            print("tmp文件夹创建失败")
    imgpath = basicpath + str(x1) + "_" + str(y1) + "_" + str(x2) + "_" + str(y2) + ".png"
    # crop里对应的数值为该位置图像在整体图片中左上和右下两个点的像素坐标
    cropped = img.crop((x1, y1, x2, y2))
    cropped.save(imgpath)
    g = open(imgpath, 'rb')
    img = base64.b64encode(g.read())
    f = random.randint(0, 9)
    if f == 1 or f == 3 or f == 5 or f == 7 or f == 9:
        time.sleep(1)  # 防止超过QPS限制 引发报错
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    params = {"image": img}
    access_token = getAuth()  # 对应申请的 access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    msg_info = ''
    if response:
        json_str = response.content.decode()
        data = json.loads(json_str)
        msg = data['words_result']
        # print(msg)
        for m in msg:
            msg_info += m.get('words') + ' '
    g.close()
    os.remove(imgpath)
    return msg_info.strip()


if __name__ == '__main__':
    res = ocr("G:/CBIB/medical-record-ocr/pic/src/test.jpg", 230, 1480, 2780, 2200)
    print(res)
