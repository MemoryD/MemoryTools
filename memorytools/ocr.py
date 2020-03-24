import pyperclip as p
import easygui as g
from PIL import Image, ImageGrab, ImageDraw
from baiduOCR import BaiduOCR
from xueersiOCR import MemoryOCR
from imagetext import ImageText
from setting import *
from utils import *


class OCR(object):
    def __init__(self, root):
        self.root = root
        self.is_pause = False
        self.newline = True
        self.mode = 'text'
        # config = read_config()
        # ocr = config['ocr']
        self.textocr = BaiduOCR(BAIDU_ACCOUNTS)
        self.formulaocr = MemoryOCR(XUEERSI_ACCOUNTS)

    def pause_ocr(self, sysTrayIcon):
        self.is_pause = not self.is_pause
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def turn_mode(self, sysTrayIcon):
        if self.mode == 'text':
            self.mode = 'formula'
        else:
            self.mode = 'text'
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def turn_newline(self, sysTrayIcon):
        self.newline = not self.newline
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def pause_text(self):
        return "开启OCR" if self.is_pause else "暂停OCR"

    def mode_text(self):
        return "识别：文本" if self.mode == 'text' else "识别：公式"

    def newline_text(self):
        return "换行：是" if self.newline else "换行：否"

    # def setting(self, sysTrayIcon):
    #     msg = "需要设置百度AI平台(https://ai.baidu.com/)的API才能进行OCR识别"
    #     title = "设置百度API"
    #     fieldNames = ["*APP_ID","*API_KEY","*SECRET_KEY"]
    #     fieldValues = []
    #     fieldValues = g.multenterbox(msg, title, fieldNames)
    #     while True:
    #         if fieldValues == None:
    #             break
    #         errmsg = ""
    #         for i in range(len(fieldNames)):
    #             option = fieldNames[i].strip()
    #             if fieldValues[i].strip() == "" and option[0] == "*":
    #                 errmsg += ("【%s】为必填项   " %fieldNames[i])
    #         if errmsg == "":
    #             break
    #         fieldValues = g.multenterbox(errmsg, title, fieldNames, fieldValues)
        
    #     if fieldValues:
    #         config = read_config()
    #         ocr = config['ocr']
    #         ocr['APP_ID'] = fieldValues[0]
    #         ocr['APP_KEY'] = fieldValues[1]
    #         ocr['SECRET_KEY'] = fieldValues[2]
    #         config['ocr'] = ocr
    #         write_config(config)
    #         self.textocr = BaiduOCR([ocr, ])

    def start(self):
        if self.is_pause:
            return
        im = ImageGrab.grabclipboard()          # 获取剪切板

        if isinstance(im, Image.Image):         # 判断是否是图片
            try:
                if self.mode == 'text':
                    text = self.textocr.ocr(im, self.newline)
                elif self.mode == 'formula':
                    pos, text = self.formulaocr.ocr(im)
                    print("位置：", pos)
                    draw = ImageDraw.Draw(im)
                    color = Color()
                    for rect in pos:
                        draw.polygon(getRect(*rect), outline=color.next())
            except Exception as e:
                text = str(e)

            p.copy('')
            ImageText(im, text)


if __name__ == '__main__':
    OCR().start()
