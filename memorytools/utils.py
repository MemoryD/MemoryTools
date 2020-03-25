import os
import re
import json
from base64 import b64decode
from io import BytesIO
from setting import *

class Color(object):
    def __init__(self):
        self.colors = COLOR
        self.index = 0
        
    def next(self):
        color = self.colors[self.index]
        self.index = (self.index + 1) % (len(self.colors))
        return color

def nonStringIterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)

def getTextLine(text):
    return len(text.split('\n'))

def getRect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

def getPic(pic_code, pic_name):
    with open(pic_name, 'wb') as image:
        image.write(b64decode(pic_code))

def img2base64(image):
    with open(image, 'rb') as bin_data:
        image_data = bin_data.read()
        image_data_base64 = base64.b64encode(image_data)
        image_data_base64 = quote(image_data_base64)
        return image_data_base64

def readConfig(name=CONFIG):
    # if name == CONFIG and not os.path.exists(name):
    #     resetConfig()

    with open(name, "r") as f:
        data = f.read()
        return json.loads(data)

def writeConfig(data, name=CONFIG):
    data = json.dumps(data)
    with open(name, "w") as f:
        f.write(data)

def resetConfig(name=CONFIG):
    writeConfig(DEFAULT_CONFIG, name)

def filterStr(sentence):
    sentence = re.sub(NOTAS, '', sentence)
    sentence = sentence.translate(REMOVE_PUNCTUATION_MAP)
    sentence = re.sub('[0-9]', '', sentence).strip()
    return sentence

def judgeLanguage(s):
    # s = unicode(s)   # python2需要将字符串转换为unicode编码，python3不需要
    s = filterStr(s)
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

def pil2bytes(im, img_type='png', b64=False):
    bf = BytesIO()
    im.save(bf, img_type)
    img = bf.getvalue()

    return img

