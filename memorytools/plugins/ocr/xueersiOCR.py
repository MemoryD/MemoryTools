# -*- coding: utf-8 -*-
"""
@file: xueersiOCR
@author: Memory
@date: 2020/10/11
@description: 学而思OCR的接口
"""
from time import sleep, time
from random import randint, choice
from PIL import Image
from hashlib import sha1
from base64 import b64encode
from urllib.parse import quote
from requests import post
from tools.utils import pil2bytes
from globals import ALPHADIG, XUEERSI_ERROR_CODES


class XueersiOCR(object):
    '''
    调用学而思AI平台的API进行OCR识别。
    app_key, app_secret 需要到学而思开放平台的官网上登录获取。
    '''
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.start_time = 0
        self.url = 'http://openapiai.xueersi.com/v1/api/img/ocr/general'

    def ocr(self, image: str, img_type='base64') -> dict:
        '''
        image: base64字符串或者url
        img_type: 如果是 base64 字符串，则为 base64, 如果是 url，则为 url
        返回值: API返回的json
        '''
        params = {
            'app_key'   : self.app_key,
            'time_stamp': str(int(time())),
            'nonce_str' : self.getNonceStr(),
        }
        params['sign'] = self.getReqSign(params, self.app_secret)
        params['img'] = image
        params['img_type'] = img_type
        params['recog_formula'] = 0

        payload = self.joinParams(params)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }

        start = time()
        r = post(self.url, data=payload, headers=headers)
        self.start_time = (start + time()) / 2

        res = r.json()

        return res

    @classmethod
    def joinParams(self, params: dict) -> str:
        '''
        用于拼接参数。因为直接传递字典会返回图片模糊的结果，待解决。
        '''
        palist = []
        for k, v in params.items():
            palist.append('%s=%s' % (k, v))
        payload = '&'.join(palist)
        return payload

    @classmethod
    def getReqSign(self, params: dict, app_secret: str) -> str:
        '''
        计算接口请求签名。
        返回40位的16进制字符串。
        '''
        sign = ''
        for key in sorted(params):
            sign += params[key]
        sign += app_secret
        sign = sha1(sign.encode('utf-8'))
        return sign.hexdigest()

    @classmethod
    def getNonceStr(self) -> str:
        '''
        返回一个长度为1~32的随机字符串。
        '''
        ns = ''
        for i in range(randint(1, 32)):
            ns += choice(ALPHADIG)
        return ns


class LatexOCR(object):
    """
    因为免费调用API的频率有限，因此构建一个多账号的OCR识别的类，
    可以提升程序处理的能力。
    accounts: 学而思AI平台的账号列表
    accounts = [{'app_key': '...', 'app_secret': '...'}, {...}, ...]
    """
    def __init__(self, accounts: list):
        # self.accounts = accounts
        self.interval = 10
        self.index = 0
        self.ocrs = []
        for acco in accounts:
            self.ocrs.append(XueersiOCR(acco['app_key'], acco['app_secret']))

    def get_api(self):
        '''返回一个接口用来进行OCR识别。'''
        xueersi = self.ocrs[self.index]

        time_pass = time() - xueersi.start_time
        if time_pass < self.interval:
            sleep(self.interval - time_pass + 0.1)

        self.index = (self.index + 1) % len(self.ocrs)
        return xueersi

    def ocr(self, image: str, img_type='base64'):
        '''OCR识别的主函数，传入一个PIL.Image对象，返回识别的文本和位置。'''
        xueersi = self.get_api()

        res = xueersi.ocr(image, img_type)
        pos = []
        code = res['code']
        if code != 0:
            if code in XUEERSI_ERROR_CODES:
                return (pos, XUEERSI_ERROR_CODES[code]['reason'])
            else:
                return (pos, "由于未知错误，识别失败！")

        if not res['data'] or 'content' not in res['data']:
            return (pos, "由于未知错误，识别失败！")

        content = res['data']['content']
        content = '\n\n'.join(content)
        pos = res['data']['recognition']['textLinePosition']

        return (pos, content)

    def latex(self, pilimg: Image, img_type='base64'):
        '''OCR识别的主函数，传入一个PIL.Image对象，返回识别的文本和位置。'''
        if isinstance(pilimg, Image.Image):
            image = quote(b64encode(pil2bytes(pilimg)))

        return self.ocr(image, img_type)
