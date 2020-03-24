from aip import AipOcr
from PIL import Image
from utils import pil2bytes
from setting import *

class BaiduOCR(object):
    """docstring for BaiduOCR"""
    def __init__(self, accounts: dict):
        self.index = 0
        self.ocrs = []
        self.mode = 'basicAccurate'
        for acco in accounts:
            self.ocrs.append(AipOcr(acco['APP_ID'], acco['APP_KEY'], acco['SECRET_KEY']))

    def ocr(self, image, newline=True):
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


        