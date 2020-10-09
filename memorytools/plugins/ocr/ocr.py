from easydict import EasyDict
from . import BaiduOCR
from . import LatexOCR
from PIL import Image, ImageGrab, ImageDraw
from tools.boxes import ImageTextBox
from globals import BAIDU_ACCOUNTS, XUEERSI_ACCOUNTS, ICON
from tools.utils import isCheckIcon, isPickIcon, getRect, Color, copyClip
from plugins import BasePlugin


class OCR(BasePlugin):
    def __init__(self, root, config):
        super(OCR, self).__init__("OCR识别", root, ICON.ocr, config)
        self.textocr = BaiduOCR(BAIDU_ACCOUNTS)
        self.mathocr = LatexOCR(XUEERSI_ACCOUNTS)

    def getConfig(self) -> EasyDict:
        return self.config

    def createMenu(self) -> tuple:
        menu_options = (
            ("开启OCR", isCheckIcon(self.config.is_ocr), self.pauseOcr, True),
            ('去除换行', isCheckIcon(not self.config.newline), self.turnNewline, True),
            ('识别文本', isPickIcon(self.config.mode == 'text'), self.textMode, False),
            ('识别公式', isPickIcon(self.config.mode == 'math'), self.mathMode, False),
        )

        return menu_options

    def pauseOcr(self, sysTrayIcon):
        self.config.is_ocr = not self.config.is_ocr
        self.root.refreshMenu()

    def textMode(self, sysTrayIcon):
        self.config.mode = 'text'
        self.root.refreshMenu()

    def mathMode(self, sysTrayIcon):
        self.config.mode = 'math'
        self.root.refreshMenu()

    def turnNewline(self, sysTrayIcon):
        self.config.newline = not self.config.newline
        self.root.refreshMenu()

    def start(self):
        if not self.config.is_ocr:
            return
        im = ImageGrab.grabclipboard()  # 获取剪切板

        if isinstance(im, Image.Image):  # 判断是否是图片
            try:
                if self.config.mode == 'text':
                    text = self.textocr.ocr(im, self.config.newline)
                elif self.config.mode == 'math':
                    pos, text = self.mathocr.latex(im)
                    print("位置：", pos)
                    draw = ImageDraw.Draw(im)
                    color = Color()
                    for rect in pos:
                        draw.polygon(getRect(*rect), outline=color.next())
            except Exception as e:
                text = str(e)

            copyClip('')
            ImageTextBox('OCR识别结果').show(im, text)


if __name__ == '__main__':
    OCR().start()
