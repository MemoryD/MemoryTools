from pathlib import Path
from easydict import EasyDict
from . import BaiduOCR
from . import LatexOCR
from PIL import Image, ImageGrab, ImageDraw
from tools.boxes import ImageTextBox
from globals import BAIDU_ACCOUNTS, XUEERSI_ACCOUNTS, ICON
from tools.utils import is_check, is_pick, get_rect, Color, copy_clip
from plugins import BasePlugin, change_config


class OCR(BasePlugin):
    def __init__(self, root):
        config_path = Path(__file__).parent / "config.json"
        super(OCR, self).__init__("OCR识别", root, ICON.ocr, config_path)
        self.text_ocr = BaiduOCR(BAIDU_ACCOUNTS)
        self.math_ocr = LatexOCR(XUEERSI_ACCOUNTS)

    def create_menu(self) -> tuple:
        menu_options = (
            ("开启OCR", is_check(self.is_ocr), self.pause_ocr, True),
            ('去除换行', is_check(not self.newline), self.turn_newline, True),
            ('识别文本', is_pick(self.mode == 'text'), self.text_mode, False),
            ('识别公式', is_pick(self.mode == 'math'), self.math_mode, False),
        )

        return menu_options

    @change_config
    def pause_ocr(self, s):
        self.is_ocr = not self.is_ocr

    @change_config
    def text_mode(self, s):
        self.mode = 'text'

    @change_config
    def math_mode(self, s):
        self.mode = 'math'

    @change_config
    def turn_newline(self, s):
        self.newline = not self.newline

    def start(self):
        if not self.is_ocr:
            return
        im = ImageGrab.grabclipboard()  # 获取剪切板

        if isinstance(im, Image.Image):  # 判断是否是图片
            try:
                if self.mode == 'text':
                    text = self.text_ocr.ocr(im, self.newline)
                elif self.mode == 'math':
                    pos, text = self.math_ocr.latex(im)
                    print("位置：", pos)
                    draw = ImageDraw.Draw(im)
                    color = Color()
                    for rect in pos:
                        draw.polygon(get_rect(*rect), outline=color.next())
            except Exception as e:
                text = str(e)

            copy_clip('')
            ImageTextBox('OCR识别结果').show(im, text)


if __name__ == '__main__':
    OCR().start()
