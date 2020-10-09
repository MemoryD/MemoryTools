from .base import BaseTrans
from .urls import YOUDAO_URL
from time import time
from random import randint
from hashlib import md5


class YoudaoTrans(BaseTrans):
    lang_map = {('zh-cn', 'en'): 'ZH_CH2EN', ('en', 'zh-cn'): 'EN2ZH_CH',
                ('zh-cn', 'ja'): 'ZH_CN2JA', ('ja', 'zh-cn'): 'JA2ZH_CH',
                ('zh-cn', 'kr'): 'ZH_CH2KR', ('kr', 'zh-cn'): 'KR2ZH_CH',
                ('zh-cn', 'fr'): 'ZH_CN2FR', ('fr', 'zh-cn'): 'FR2ZH_CH',
                ('zh-cn', 'ru'): 'ZH_CH2RU', ('ru', 'zh-cn'): 'RU2ZH_CH',
                ('zh-cn', 'sp'): 'ZH_CN2SP', ('sp', 'zh-cn'): 'SP2ZH_CH'}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            # 'X-Requested-With': 'XMLHttpRequest',
            "Referer": "http://fanyi.youdao.com/",
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "Cookie": "OUTFOX_SEARCH_USER_ID_NCOO=1674353290.232588;"
        }

    def __init__(self):
        super(YoudaoTrans, self).__init__(YOUDAO_URL)

    def constructParams(self, sentence, src, dest):
        if (src, dest) in self.lang_map:
            trans_type = self.langMap[(src, dest)]
        else:
            trans_type = 'AUTO'

        params = {'doctype': 'json', 'type': trans_type, 'i': sentence}

        return params

    def getParams(self, sentence, src, dest):
        # src = src or 'AUTO'
        # dest = dest or 'AUTO'
        slat = str(int(time()*10000) + randint(1, 10))
        sign_text = "fanyideskweb" + sentence + slat + "ebSeFb%=XZ%T[KZ)c(sy!"
        sign_text = sign_text.encode('utf-8')
        sign = md5(sign_text).hexdigest()

        params = {
                    'i': sentence,
                    'from': src or 'AUTO',
                    'to': dest or 'AUTO',
                    'smartresult': 'dict',
                    'client': 'fanyideskweb',
                    'salt': slat,
                    'sign': sign,
                    # 'ts': '1585286292515',
                    # 'bv': '70244e0061db49a9ee62d341c5fed82a',
                    'doctype': 'json',
                    'version': '2.1',
                    'keyfrom': 'fanyi.web',
                    'action': 'FY_BY_CLICKBUTTION',
                    "typoResult": "false",
                    }
        return params

    def translate(self, sentence: str, src=None, dest=None) -> str:
        params = self.getParams(sentence, src, dest)
        print(params)

        res = self.getData(params, self.headers)

        return res

        # if 'errorCode' in res and res['errorCode'] != 0:
        #     return '未知错误，翻译失败！'

        # text_list = []
        # data_list = res['translateResult']
        # for data in data_list:
        #     text_list += data

        # text_list = [t['tgt'] for t in text_list]
        # text = ' '.join(text_list)
        # return text


if __name__ == '__main__':
    t = YoudaoTrans().translate('你好')
    print(t)
    # while True:
    #     s = input('input: ')
    #     print(t.translate(s))
