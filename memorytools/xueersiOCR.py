import time
import hashlib
import requests
import random
from PIL import Image, ImageDraw
from base64 import b64encode
from urllib.parse import quote
from requests.exceptions import ConnectionError
from utils import *
from setting import *

ALPHADIG = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def img2base64(image):
    with open(image, 'rb') as bin_data:
        image_data = bin_data.read()
        image_data_base64 = base64.b64encode(image_data)
        image_data_base64 = quote(image_data_base64)
        return image_data_base64


class XueersiOCR(object):
    '''
    调用学而思AI平台的API进行OCR文字识别
    '''
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.start_time = 0
        self.url = 'http://openapiai.xueersi.com/v1/api/img/ocr/general'

    def ocr(self, image: str, img_type='base64')->dict:
        '''
        image 是base64字符串或者url
        '''
        params = {
            'app_key'    : self.app_key,
            'time_stamp' : str(int(time.time())),
            'nonce_str'  : self.getNonceStr(),
        }
        params['sign'] = self.getReqSign(params, self.app_secret)
        params['img'] = image
        params['img_type'] = img_type
        params['recog_formula'] = 0

        payload = self.join_params(params)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }

        start = time.time()
        r = requests.post(self.url, data=payload, headers=headers)
        self.start_time = (start + time.time()) / 2

        res = r.json()
        # print(res)
        return res

    @classmethod
    def join_params(self, params: dict)->str:
        '''
        用于拼接参数。因为直接传递字典会返回图片模糊的结果，待解决。
        '''
        palist = []
        for k, v in params.items():
            palist.append('%s=%s'%(k,v))
        payload = '&'.join(palist)
        return payload

    @classmethod
    def getReqSign(self, params:dict, app_secret: str)->str:
        '''
        计算接口请求签名。
        返回40位的16进制字符串。
        '''
        sign = ''
        for key in sorted(params):
            sign += params[key]
        sign += app_secret
        sign = hashlib.sha1(sign.encode('utf-8'))
        return sign.hexdigest()

    @classmethod
    def getNonceStr(self)->str:
        '''
        返回一个长度为1~32的随机字符串。
        '''
        ns = ''
        for i in range(random.randint(1, 32)):
            ns += random.choice(ALPHADIG)
        return ns


class MemoryOCR(object):
    """docstring for MemoryOCR"""
    def __init__(self, accounts: list):
        # self.accounts = accounts
        self.interval = 10
        self.index = 0
        self.ocrs = []
        for acco in accounts:
            self.ocrs.append(XueersiOCR(acco['app_key'], acco['app_secret']))

    def ocr(self, image: str, img_type='base64'):
        if isinstance(image, Image.Image):
            image = quote(b64encode(pil2bytes(image)))

        xueersi = self.ocrs[self.index]
        time_pass = time.time() - xueersi.start_time
        if time_pass < self.interval:
            time.sleep(self.interval - time_pass + 0.1)

        self.index = (self.index + 1) % len(self.ocrs)
        res = xueersi.ocr(image, img_type)
        code = res['code']
        if code != 0:
            if code in ERROR_CODES:
                return ([], ERROR_CODES[code]['reason'])
            else:
                return ([], "由于未知错误，识别失败！")
        if not res['data'] or 'content' not in res['data']:
            return ([], "由于未知错误，识别失败！")

        content = res['data']['content']
        content = '\n\n'.join(content)
        pos = res['data']['recognition']['textLinePosition']
        return (pos, content)
        

def getRect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

if __name__ == '__main__':
    mocr = MemoryOCR(XUEERSI_ACCOUNTS)
    for i in range(1, 7):
        image_path = '.\\src\\new_new_test%s.png' % i
        # xueersi = XueersiOCR(XUEERSI_ACCOUNTS[0]['app_key'], XUEERSI_ACCOUNTS[0]['app_secret'])
        img = img2base64(image_path)
        rects = mocr.ocr(img)['data']['recognition']['textLinePosition']
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        for rect in rects:
            draw.polygon(getRect(*rect), outline=(255,0,0))
        image.save(image_path.replace('test', 'reg'), 'png')
        # time.sleep(11)
        
        # image = Image.open(image_path)
        # w, h = image.size
        # image = image.resize((int(w*0.7), h))
        # image.save(image_path.replace('test', 'new_test'), 'png')

    # mocr = MemoryOCR(XUEERSI_ACCOUNTS)
    # for _ in range(5):
    #     for i in range(1, 5):
    #         img = img2base64('test'+str(i)+'.png')
    #         res = mocr.ocr(img)
    #         print(res)

