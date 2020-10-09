import os
import re
import json
from time import sleep
from pyperclip import paste, copy
from base64 import b64decode, b64encode
from urllib.parse import quote
from io import BytesIO
from easydict import EasyDict
from globals import *


class Color(object):
    def __init__(self):
        self.colors = COLOR
        self.index = 0

    def next(self):
        color = self.colors[self.index]
        self.index = (self.index + 1) % (len(self.colors))
        return color


def pasteClip():
    for i in range(3):
        try:
            text = paste()
            return text
        except Exception as e:
            if i == 2:
                return str(e)
            sleep(0.1)


def copyClip(text):
    try:
        copy(text)
    except Exception as e:
        print(e)


def getTextLine(text: str):
    """返回所给的文本有几行"""
    return len(text.split('\n'))


def getRect(x1: int, y1: int, x2: int, y2: int):
    """给定矩形框的左上角和右下角坐标，返回四个角的坐标"""
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def pil2bytes(im, img_type='png', b64=False):
    """将PIL.Image格式的图像转化为二进制数据"""
    bf = BytesIO()
    im.save(bf, img_type)
    img = bf.getvalue()

    return img


def bs64toImg(pic_code, pic_name):
    """将bs64编码的数据写到文件中"""
    with open(pic_name, 'wb') as image:
        image.write(b64decode(pic_code))


def resizeImg(img, max_w: int, max_h: int):
    """
    对img进行缩放，使其长宽不超过给定的 max_w 和 max_h
    """
    img_w, img_h = img.size
    if img_w < max_w and img_h < max_h:
        return img

    if img_w * max_h > img_h * max_w:
        new_w = max_w
        new_h = img_h * (new_w / img_w)
        img = img.resize((int(new_w), int(new_h)))
    else:
        new_h = max_h
        new_w = img_w * (new_h / img_h)
        img = img.resize((int(new_w), int(new_h)))

    return img


# def getSrc(pic: str):
#     """返回对应资源的完整路径"""
#     path = os.path.join(ICON_PATH, pic)
#     file = os.path.abspath(path)
#
#     if not os.path.exists(ICON_PATH):
#         os.makedirs(ICON_PATH)
#     if not os.path.exists(file):
#         if pic in ICONS:
#             bs64toImg(ICONS[pic], file)
#
#     return file


def isCheckIcon(check: bool):
    """是否选中（两种状态）"""
    return ICON.check if check else None


def isPickIcon(pick: bool):
    """是否被选中（多项中的一个）"""
    return ICON.pick if pick else None


def img2base64(image: str):
    """将图像从文件中读取出来并转化为base64编码"""
    with open(image, 'rb') as bin_data:
        image_data = bin_data.read()
        image_data_base64 = b64encode(image_data)
        image_data_base64 = quote(image_data_base64)
        return image_data_base64


# def readConfig(config=PATH.config) -> EasyDict:
#     """
#     读配置文件
#     """
#     if config == PATH.config and not os.path.exists(name):
#         resetConfig()
#     try:
#         with open(name, "r", encoding="utf-8") as f:
#             data = f.read()
#             return EasyDict(json.loads(data))
#     except Exception as e:
#         print(e)
#         return DEFAULT_CONFIG
#
#
# def writeConfig(data: dict, name=CONFIG):
#     """
#     写配置文件
#     """
#     try:
#         data = json.dumps(data, indent=4, ensure_ascii=False)
#         with open(name, "w", encoding="utf-8") as f:
#             f.write(data)
#     except Exception as e:
#         print(e)
#
#
# def resetConfig(name=CONFIG):
#     """
#     重置配置文件
#     """
#     writeConfig(DEFAULT_CONFIG, name)


def filterStr(sentence: str):
    """
    过滤掉字符串中的标点符号
    """
    sentence = re.sub(NOTAS, '', sentence)
    sentence = sentence.translate(PUNCTUATION_MAP)
    sentence = re.sub('[0-9]', '', sentence).strip()
    sentence = re.sub(' ', '', sentence).strip()
    return sentence


def judgeLanguage(sentence: str):
    """
    判断一句话里面英文和中文的占比
    """
    sentence = filterStr(sentence)

    if sentence == '':
        return (None, 0)

    en_pattern = re.compile(u"[a-zA-Z]")
    zh_pattern = re.compile(u"[\u4e00-\u9fa5]")

    en = re.findall(en_pattern, sentence)
    zh = re.findall(zh_pattern, sentence)
    en_num = len(en) // 3
    zh_num = len(zh)

    total = en_num + zh_num
    if total == 0:
        return None, 0

    if en_num > zh_num:
        return 'en', en_num / total
    else:
        return 'zh-cn', zh_num / total


def count_code():
    """计算当前文件夹里面python代码的行数"""
    files = os.listdir('..\\')
    total = 0
    for file in files:
        if not os.path.isfile(file):
            continue
        name, ext = os.path.splitext(file)
        if ext != '.py':
            continue
        with open(file, 'r', encoding='utf-8') as f:
            line = len(f.readlines())
        total += line
        print("%s : %d" % (file, line))
    print("total :", total)


if __name__ == '__main__':
    count_code()
