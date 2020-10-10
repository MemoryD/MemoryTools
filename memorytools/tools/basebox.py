# -*- coding: utf-8 -*-
"""
@file: basebox.py
@author: Memory
@date: 2020/3/23
@description: 自定义弹出框的基类，可以在插件中调用
"""

from tkinter import Tk, END
from tkinter.ttk import Button, Frame
from tools.utils import copy_clip
from globals import ICON


class BaseBox(Tk):
    """
    弹出框的基类，默认居中显示，只有一个取消按钮，
    子类可以添加其他的组件
    """
    def __init__(self, buttons=[], title='Memory Tools'):
        super(BaseBox, self).__init__()
        self.set_window(title)
        self.set_button(buttons)

    def set_window(self, title: str):
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.title(title)
        self.resizable(False, False)
        self.iconbitmap(ICON.icon)

        min_w = self.screen_w // 3
        min_h = self.screen_h // 3
        self.minsize(min_w, min_h)

    def set_button(self, buttons: list):
        '''
        定义底部按钮
        '''
        self.btn_frame = Frame(self)
        for text, command in buttons:
            btn = Button(self.btn_frame, text=text, cursor='hand2', command=command)
            btn.pack(side='left', padx=20, pady=10)

        self.cancel_bth = Button(self.btn_frame, text="取消", cursor='hand2', command=self.destroy)
        self.cancel_bth.pack(side='left', padx=20, pady=10)
        self.btn_frame.pack(side='bottom')

    def start(self, show=True):
        '''
        设置窗口位置，并运行显示消息框
        '''
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        pos_x = (self.screen_w - width)//2
        pos_y = max(0, (self.screen_h - height)//2-50)
        size = '+%d+%d' % (pos_x, pos_y)
        self.geometry(size)
        self.mainloop()

    def copy(self):
        txt = self.textbox.get("1.0", END)
        copy_clip(txt)
        self.destroy()
