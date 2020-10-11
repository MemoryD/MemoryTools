# -*- coding: utf-8 -*-
from pathlib import Path
from . import BaiduOCR
from . import LatexOCR
from PIL import Image, ImageGrab, ImageDraw
from .ocrbox import OcrBox
from tools.logger import logger
from globals import BAIDU_ACCOUNTS, XUEERSI_ACCOUNTS, ICON, PATH
from tools.utils import is_check, is_pick, get_rect, Color, copy_clip
from plugins import BasePlugin, change_config


class OCR(BasePlugin):
    def __init__(self, root):
        # config_path = Path(__file__).parent / "config.json"
        config_path = PATH.config / ("%s.json" % Path(__file__).stem)
        super(OCR, self).__init__("OCR识别", root, ICON.ocr, config_path)
        self.config = self.init_config()
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

    def create_default_config(self) -> dict:
        config = {
            "is_ocr": True,
            "newline": False,
            "mode": "text"
        }
        return config

    @change_config
    def pause_ocr(self, s):
        self.is_ocr = not self.is_ocr
        if self.is_ocr:
            logger.info("[OCR识别] 开启OCR识别")
        else:
            logger.info("[OCR识别] 关闭OCR识别")

    @change_config
    def text_mode(self, s):
        self.mode = 'text'
        logger.info("[OCR识别] 切换OCR识别模式为: 文本")

    @change_config
    def math_mode(self, s):
        self.mode = 'math'
        logger.info("[OCR识别] 切换OCR识别模式为: 公式")

    @change_config
    def turn_newline(self, s):
        self.newline = not self.newline
        if not self.newline:
            logger.info("[OCR识别] 开启去除换行")
        else:
            logger.info("[OCR识别] 关闭去除换行")

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
            OcrBox('OCR识别结果').show(im, text)


if __name__ == '__main__':
    OCR().start()
