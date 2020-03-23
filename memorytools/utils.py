import os
import re
import json
import time
from base64 import b64decode
from setting import *

class Accounts(object):
    def __init__(self, accounts:list, interval=10):
        self.index = 0
        self.interval = interval
        # self.len = len(accounts)
        self.accounts = accounts
        for acco in self.accounts:
            acco['time'] = 0

    def getNext(self):
        acco = self.accounts[self.index]
        time_pass = time.time() - acco['time']
        if time_pass < self.interval:
            time.sleep(self.interval - time_pass)
        self.index = (self.index + 1) % len(self.accounts)
        acco['time'] = time.time()
        return acco['app_key'], acco['app_secret']

def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)


def get_pic(pic_code, pic_name):
    with open(pic_name, 'wb') as image:
        image.write(b64decode(pic_code))


def read_config(name=CONFIG):
    if name == CONFIG and not os.path.exists(name):
        reset_config()

    with open(name, "r") as f:
        data = f.read()
        return json.loads(data)

def write_config(data, name=CONFIG):
    data = json.dumps(data)
    with open(name, "w") as f:
        f.write(data)

def reset_config(name=CONFIG):
    write_config(DEFAULT_CONFIG, name)

def filter_str(sentence):
    sentence = re.sub(NOTAS, '', sentence)
    sentence = sentence.translate(REMOVE_PUNCTUATION_MAP)
    sentence = re.sub('[0-9]', '', sentence).strip()
    return sentence

def judge_language(s):
    # s = unicode(s)   # python2需要将字符串转换为unicode编码，python3不需要
    s = filter_str(s)
    re_words = re.compile(u"[a-zA-Z]")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub('[a-zA-Z]', '', s).strip()
    if len(res2) <= 0:  # 表示s是纯英文
        return 'en'

    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u4e00-\u9fa5]+", '', s).strip()
    if len(res2) <= 0:  # 表示s是纯中文
        return 'zh-cn'

    return 'both'

if __name__ == '__main__':
    a = Accounts(XUEERSI_ACCOUNTS)
    for i in range(10):
        print(a.getNext())
        print(time.time())
        time.sleep(1)

    # while True:
    #     text = input('输入要识别的文字： ')
    #     print(judge_language(text, 'zh-cn'))
