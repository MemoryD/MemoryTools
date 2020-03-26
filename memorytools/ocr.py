import pyperclip as p
from PIL import Image, ImageGrab, ImageDraw
from baiduOCR import BaiduOCR
from xueersiOCR import LatexOCR
from boxes import ImageTextBox
from setting import BAIDU_ACCOUNTS, XUEERSI_ACCOUNTS
from utils import isCheckIcon, isPickIcon, getRect, Color


class OCR(object):
    def __init__(self, root):
        self.root = root
        self.is_ocr = True
        self.newline = True
        self.mode = 'text'
        self.textocr = BaiduOCR(BAIDU_ACCOUNTS)
        self.formulaocr = LatexOCR(XUEERSI_ACCOUNTS)

    def setConfig(self, config: dict):
        if 'is_ocr' in config:
            self.is_ocr = config['is_ocr']
        if 'newline' in config:
            self.newline = config['newline']
        if 'mode' in config:
            self.mode = config['mode']

    def getConfig(self) -> dict:
        config = {
            'is_ocr': self.is_ocr,
            'newline': self.newline,
            'mode': self.mode
        }
        return config

    def createMenu(self) -> tuple:
        menu_options = (
                        ("开启OCR", isCheckIcon(self.is_ocr), self.pauseOcr, True),
                        ('去除换行', isCheckIcon(not self.newline), self.turnNewline, True),
                        ('识别文本', isPickIcon(self.mode=='text'), self.textMode, False),
                        ('识别公式', isPickIcon(self.mode=='formula'), self.formulaMode, False),
                        )

        return menu_options

    def pauseOcr(self, sysTrayIcon):
        self.is_ocr = not self.is_ocr
        self.root.refreshMenu()

    def textMode(self, sysTrayIcon):
        self.mode = 'text'
        self.root.refreshMenu()

    def formulaMode(self, sysTrayIcon):
        self.mode = 'formula'
        self.root.refreshMenu()

    def turnNewline(self, sysTrayIcon):
        self.newline = not self.newline
        self.root.refreshMenu()

    def start(self):
        if not self.is_ocr:
            return
        im = ImageGrab.grabclipboard()          # 获取剪切板

        if isinstance(im, Image.Image):         # 判断是否是图片
            try:
                if self.mode == 'text':
                    text = self.textocr.ocr(im, self.newline)
                elif self.mode == 'formula':
                    pos, text = self.formulaocr.latex(im)
                    print("位置：", pos)
                    draw = ImageDraw.Draw(im)
                    color = Color()
                    for rect in pos:
                        draw.polygon(getRect(*rect), outline=color.next())
            except Exception as e:
                text = str(e)

            p.copy('')
            ImageTextBox('OCR识别结果').show(im, text)


if __name__ == '__main__':
    OCR().start()
