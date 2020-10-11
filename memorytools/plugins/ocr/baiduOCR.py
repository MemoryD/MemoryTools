# -*- coding: utf-8 -*-
from aip import AipOcr
from PIL import Image
from tools.utils import pil2bytes
from globals import BAIDU_ERROR_CODES


class BaiduOCR(object):
    """
    因为免费调用API的次数以及频率有限，因此利用百度官方提供的API构建
    一个多账号的OCR识别的类，可以提升程序处理的能力。
    传入一个账号的列表，可以根据额度自动切换识别的模式。

    accounts: 百度AI平台的账号列表
    accounts = [{'APP_ID': '...', 'APP_KEY': '...', 'SECRET_KEY': '...'}, {...}, ...]
    """
    def __init__(self, accounts: list):
        self.index = 0
        self.ocrs = []
        self.mode = 'basicAccurate'
        for acco in accounts:
            self.ocrs.append(AipOcr(acco['APP_ID'], acco['APP_KEY'], acco['SECRET_KEY']))

    def ocr(self, image: Image, newline=True) -> str:
        '''OCR识别的主函数，传入一个PIL.Image对象，返回识别的文本。'''
        if self.mode == 'None':
            return '当天配额已用完，请更换API或明天再试！'

        if isinstance(image, Image.Image):
            image = pil2bytes(image)

        textocr = self.ocrs[self.index]
        self.index = (self.index + 1) % (len(self.ocrs))

        if self.mode == 'basicAccurate':
            dic_result = textocr.basicAccurate(image)
        elif self.mode == 'basicGeneral':
            dic_result = textocr.basicGeneral(image)

        if 'error_code' in dic_result:
            code = dic_result['error_code']
            msg = BAIDU_ERROR_CODES[code]
            if code == 17:
                if self.mode == 'basicAccurate':
                    self.mode = 'basicGeneral'
                    dic_result = textocr.basicGeneral(image)
                elif self.mode == 'basicGeneral':
                    self.mode = 'None'
                    return msg
            else:
                return msg

        if 'words_result' not in dic_result:
            return '由于未知错误识别失败，请稍候重试！'

        res = dic_result['words_result']

        res = [words['words'] for words in res]

        if newline:
            res = '\n'.join(res)
        else:
            res = ''.join(res)

        return res
