# -*- coding: utf-8 -*-
from tkinter.ttk import Label
from tools.basebox import BaseBox


class AlertBox(BaseBox):
    """
    用于显示警告信息
    """
    def __init__(self, title='AlertBox'):
        super(AlertBox, self).__init__([], title)

    def show(self, text: str, button=None):
        self.minsize(self.screen_w//3, self.screen_h//5)
        label = Label(self, text=text,  font=("微软雅黑", 12))
        label.pack(padx=10, pady=50)
        if button:
            self.cancel_bth.config(text=button)
        self.start()
