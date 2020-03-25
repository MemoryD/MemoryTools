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
    '''返回所给的文本有几行'''
    return len(text.split('\n'))

def getRect(x1, y1, x2, y2):
    '''给定矩形框的左上角和右下角坐标，返回四个角的坐标'''
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

def bs64toImg(pic_code, pic_name):
    '''将bs64编码的数据写到文件中'''
    with open(pic_name, 'wb') as image:
        image.write(b64decode(pic_code))

def getSrc(pic):
    '''返回对应资源的完整路径'''
    path = os.path.join(SRC_PATH, pic)
    return os.path.abspath(path)

def isCheckIcon(check):
    '''是否选中（两种状态）'''
    return getSrc('check.ico') if check else None

def isPickIcon(pick):
    '''是否被选中（多项中的一个）'''
    return getSrc('pick.ico') if pick else None

def img2base64(image):
    '''将图像从文件中读取出来并转化为base64编码'''
    with open(image, 'rb') as bin_data:
        image_data = bin_data.read()
        image_data_base64 = base64.b64encode(image_data)
        image_data_base64 = quote(image_data_base64)
        return image_data_base64

def readConfig(name=CONFIG):
    '''读配置文件'''
    # if name == CONFIG and not os.path.exists(name):
    #     resetConfig()

    with open(name, "r") as f:
        data = f.read()
        return json.loads(data)

def writeConfig(data, name=CONFIG):
    '''写配置文件'''
    data = json.dumps(data)
    with open(name, "w") as f:
        f.write(data)

def resetConfig(name=CONFIG):
    '''重置配置文件'''
    writeConfig(DEFAULT_CONFIG, name)

def filterStr(sentence):
    '''过滤掉字符串中的标点符号'''
    sentence = re.sub(NOTAS, '', sentence)
    sentence = sentence.translate(REMOVE_PUNCTUATION_MAP)
    sentence = re.sub('[0-9]', '', sentence).strip()
    sentence = re.sub(' ', '', sentence).strip()
    return sentence

def judgeLanguage(s):
    '''判断一句话里面英文和中文的占比'''
    s = filterStr(s)

    en_pattern = re.compile(u"[a-zA-Z]")
    zh_pattern = re.compile(u"[\u4e00-\u9fa5]")

    en = re.findall(en_pattern, s)
    zh = re.findall(zh_pattern, s)
    en_num = len(en) // 3
    zh_num = len(zh)
    total = en_num + zh_num
    if en_num > zh_num:
        return ('en', en_num / total)
    else:
        return ('zh-cn', zh_num / total)
    # return (en_num / total, zh_num / total)

    # print(len(s))
    # re_words = re.compile(u"[a-zA-Z]")
    # res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    # print(res)
    # res2 = re.sub('[a-zA-Z]', '', s).strip()
    # if len(res2) <= 0:  # 表示s是纯英文
    #     return 'en'

    # re_words = re.compile(u"[\u4e00-\u9fa5]")
    # res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    # print(res)
    # res2 = re.sub(u"[\u4e00-\u9fa5]", '', s).strip()
    # if len(res2) <= 0:  # 表示s是纯中文
    #     return 'zh-cn'

    # return 'both'

def pil2bytes(im, img_type='png', b64=False):
    '''将PIL.Image格式的图像转化为二进制数据'''
    bf = BytesIO()
    im.save(bf, img_type)
    img = bf.getvalue()

    return img

if __name__ == '__main__':
    while True:
        s = input("输入：")
        print(judgeLanguage(s))
