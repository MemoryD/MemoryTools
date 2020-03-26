'''
@file: boxes.py
@author: Memory
@date: 2020/3/23
@description: 自定义的一些弹出框
'''
import os
import pyperclip as p
from PIL import ImageTk
from tkinter import Tk, END
from tkinter.ttk import Label, Button, Frame
from tkinter.scrolledtext import ScrolledText, Text
from utils import getTextLine, resizeImg


class BaseBox(Tk):
    """弹出框的基类"""
    def __init__(self, buttons=[], title='Memory Tools'):
        super(BaseBox, self).__init__()
        self.setWindow(title)
        self.setButton(buttons)

    def setWindow(self, title: str):
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.title(title)
        self.resizable(False, False)
        if os.path.exists("icon.ico"):
            self.iconbitmap('icon.ico')

        min_w = self.screen_w // 3
        min_h = self.screen_h // 3
        self.minsize(min_w, min_h)

    def setButton(self, buttons: list):
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
        p.copy(txt)
        self.destroy()


class TextTextBox(BaseBox):
    def __init__(self, title='MemoryBox'):
        buttons = [('复制', self.copy), ]
        super(TextTextBox, self).__init__(buttons, title)

    def show(self, src: str, dest: str):
        h1 = min(10, max(5, getTextLine(src)+1))
        h2 = min(10, max(5, getTextLine(dest)+1))

        self.src_text = ScrolledText(self, height=h1, background='#ffffff', font=("微软雅黑", 11))
        self.textbox = ScrolledText(self, height=h2, background='#ffffff', font=("微软雅黑", 11))

        self.src_text.insert(END, str(src))
        self.src_text.config(state='disabled')
        self.textbox.insert(END, str(dest))

        self.src_text.pack(side='top', padx=10, pady=10)
        self.textbox.pack(side='top', padx=10, pady=10)

        self.start()


class ImageBox(BaseBox):
    def __init__(self, title='MemoryBox'):
        super(ImageBox, self).__init__([], title)

    def show(self, img):
        img = resizeImg(img, self.screen_w//3, 100000)
        w, h = img.size
        self.geometry('%dx%d' % (w+20, self.screen_h*2//3))
        image = ImageTk.PhotoImage(image=img)
        text = Text(self, height=100)
        text.image_create(END, image=image)
        text.pack(side='top', padx=10, fill='y')
        self.cancel_bth.config(text='确定')
        self.start()


class LabelBox(BaseBox):
    """docstring for LabelBox"""
    def __init__(self, title='MemoryBox'):
        super(LabelBox, self).__init__([], title)

    def show(self, text: str, button=None):
        self.minsize(self.screen_w//3, self.screen_h//5)
        label = Label(self, text=text,  font=("微软雅黑", 12))
        label.pack(padx=10, pady=50)
        if button:
            self.cancel_bth.config(text=button)
        self.start()


class ImageTextBox(BaseBox):
    '''用来显示一张图片和一个文本框，会根据图片的大小和比例调整排列的方式'''
    def __init__(self, title='MemoryBox'):
        buttons = [('复制', self.copy), ]
        super(ImageTextBox, self).__init__(buttons, title)

    def setSize(self, img):
        '''
        对图片进行处理，并限制窗口大小
        '''
        img_w, img_h = img.size
        aspect_ratio = self.screen_w / self.screen_h

        if img_w > img_h * aspect_ratio:
            w, h = self.screen_w * 0.9, self.screen_h * 0.35
            img = resizeImg(img, w, h)
            img_w, img_h = img.size
            width = max(self.screen_w // 3, img_w+20)
            self.maxsize(width, int(self.screen_h*0.9))
        else:
            w, h = self.screen_w * 0.45, self.screen_h * 0.7
            img = resizeImg(img, w, h)
            img_w, img_h = img.size
            width = max(self.screen_w // 3, 2 * img_w + 70)
            self.maxsize(width, int(self.screen_h*0.9))

        return img

    def show(self, img, txt: str):
        '''
        显示
        '''
        img = self.setSize(img)
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


if __name__ == '__main__':
    LabelBox().show("虽然你关掉了休息提醒，但还是要注意身体！", '确认')
