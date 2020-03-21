import os
import functools
import easygui as g
from ocr import OCR
from alert import Alert
from copytrans import CopyTrans
from systrayicon import SysTrayIcon
from pic import icon_ico
from utils import *
from setting import *


class Root(object):
    def __init__(self):
        self.alert = Alert(self)
        self.ct = CopyTrans(self)
        self.ocr = OCR(self)
        self.icon = 'icon.ico'
        if not os.path.exists(self.icon):
            get_pic(icon_ico, self.icon)

    def about(self, sysTrayIcon):
        g.textbox(msg=ABOUT_MSG, title="关于", text=ABOUT_TEXT)

    def create_menu(self):
        self.menu_options = (
                            ('复制翻译', None, (
                                        (self.ct.pause_text(), None, self.ct.pause_trans),
                                        (self.ct.language_text(), None, self.ct.turn_language),
                                        (self.ct.strict_text(), None, self.ct.turn_strict)
                                        )),
                            ('OCR识别', None, (
                                        (self.ocr.pause_text(), None, self.ocr.pause_ocr),
                                        ('API设置', None, self.ocr.setting),
                                        )),
                            ('休息提醒', None, (
                                        (self.alert.alert_text(), None, self.alert.pause_alert),
                                        ('更改时间', None, self.alert.change_time),
                                        )),
                            ('关于', None, self.about)
                            )
        return self.menu_options

    def bye(self, sysTrayIcon):
        pass

    def run(self):
        self.ct.run()
        self.alert.run()
        self.ocr.run()
        SysTrayIcon(self.icon, HOVER_TEXT, self.create_menu(), on_quit=self.bye, default_menu_index=1)


if __name__ == '__main__':
    Root().run()
