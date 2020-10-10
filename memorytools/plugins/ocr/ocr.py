from pathlib import Path

from easydict import EasyDict
from . import BaiduOCR
from . import LatexOCR
from PIL import Image, ImageGrab, ImageDraw
from tools.boxes import ImageTextBox
from globals import BAIDU_ACCOUNTS, XUEERSI_ACCOUNTS, ICON
from tools.utils import isCheckIcon, isPickIcon, getRect, Color, copyClip
from plugins import BasePlugin, change_config


class OCR(BasePlugin):
    def __init__(self, root):
        config_path = Path(__file__).parent / "config.json"
        super(OCR, self).__init__("OCR识别", root, ICON.ocr, config_path)
        self.textocr = BaiduOCR(BAIDU_ACCOUNTS)
        self.mathocr = LatexOCR(XUEERSI_ACCOUNTS)

    def create_menu(self) -> tuple:
        menu_options = (
            ("开启OCR", isCheckIcon(self.is_ocr), self.pauseOcr, True),
            ('去除换行', isCheckIcon(not self.newline), self.turnNewline, True),
            ('识别文本', isPickIcon(self.mode == 'text'), self.textMode, False),
            ('识别公式', isPickIcon(self.mode == 'math'), self.mathMode, False),
        )

        return menu_options

    @change_config
    def pauseOcr(self, s):
        self.is_ocr = not self.is_ocr

    @change_config
    def textMode(self, s):
        self.mode = 'text'

    @change_config
    def mathMode(self, s):
        self.mode = 'math'

    @change_config
    def turnNewline(self, s):
        self.newline = not self.newline

    def start(self):
        if not self.is_ocr:
            return
        im = ImageGrab.grabclipboard()  # 获取剪切板

        if isinstance(im, Image.Image):  # 判断是否是图片
            try:
                if self.mode == 'text':
                    text = self.textocr.ocr(im, self.newline)
                elif self.mode == 'math':
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
