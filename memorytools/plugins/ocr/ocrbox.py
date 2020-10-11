# -*- coding: utf-8 -*-
"""
@file: ocrbox
@author: Memory
@date: 2020/10/11
@description: ocr弹出框的定义
"""
from tkinter import Label, END
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk
from tools.basebox import BaseBox


class OcrBox(BaseBox):
    """
    用来显示一张图片和一个文本框，会根据图片的大小和比例调整排列的方式
    """
    def __init__(self, title='OcrBox'):
        buttons = [('复制', self.copy), ]
        super(OcrBox, self).__init__(buttons, title)

    def resize_img(self, img, max_w: int, max_h: int):
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

    def set_size(self, img):
        """
        对图片进行处理，并限制窗口大小
        """
        img_w, img_h = img.size
        aspect_ratio = self.screen_w / self.screen_h

        if img_w > img_h * aspect_ratio:
            w, h = self.screen_w * 0.9, self.screen_h * 0.35
            img = self.resize_img(img, w, h)
            img_w, img_h = img.size
            width = max(self.screen_w // 3, img_w+20)
            self.maxsize(width, int(self.screen_h*0.9))
        else:
            w, h = self.screen_w * 0.45, self.screen_h * 0.7
            img = self.resize_img(img, w, h)
            img_w, img_h = img.size
            width = max(self.screen_w // 3, 2 * img_w + 70)
            self.maxsize(width, int(self.screen_h*0.9))

        return img

    def show(self, img, txt: str):
        """
        显示
        """
        img = self.set_size(img)
        w, h = img.size

        self.tkImage = ImageTk.PhotoImage(image=img)
        self.label = Label(self, image=self.tkImage)
        self.textbox = ScrolledText(self, height=10, background='#ffffff', font=("微软雅黑", 11))
        self.textbox.insert(END, txt)

        aspect_ratio = self.screen_w / self.screen_h
        if w >= h * aspect_ratio:
            self.label.pack(side='top', padx=10, pady=10)
            self.textbox.pack(side='top', padx=10, pady=10, fill='both')
        else:
            self.label.pack(side='left', padx=10, pady=10)
            self.textbox.pack(side='right', padx=10, pady=10, fill='both')

        self.start()
