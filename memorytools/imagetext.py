'''
@file: imagetext.py
@author: Memory
@date: 2020/3/23
@description: 
'''
import os
import pyperclip as p
from xueersiOCR import MemoryOCR
from setting import *
from io import BytesIO
from base64 import b64encode
from urllib.parse import quote
from threading import Thread
from PIL import Image, ImageTk, ImageGrab, ImageDraw
from time import strftime, localtime, time, sleep
from tkinter import Tk, END, TOP, DISABLED, Menu, INSERT, X, LEFT, Checkbutton, BOTTOM
from tkinter.ttk import Notebook, Label, Button, Frame, LabelFrame
from tkinter.scrolledtext import ScrolledText, Text

class TextText(Tk):
    def __init__(self, img, txt):
        pass

class ImageText(Tk):
    def __init__(self, img, txt):
        Tk.__init__(self)
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.set_window()
        self.img =  self.set_size(img)
        self.set_button()
        self.show(self.img, txt)
        self.center_window()
        self.mainloop()

    def set_window(self):

        self.title('OCR识别结果')
        self.resizable(False, False)
        if os.path.exists("icon.ico"):
            self.iconbitmap('icon.ico')


        min_w = self.screen_w // 3
        min_h = self.screen_h // 3
        self.minsize(min_w, min_h)

    def center_window(self):
        '''
        窗口居中
        '''
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        print("窗口大小: (%s ,%s)" % (width, height))
        size = '+%d+%d' % ((self.screen_w - width)/2, (self.screen_h - height)/2)
        self.geometry(size)

    def resize_img(self, img, max_w, max_h):
        '''
        对img进行缩放，使其长宽不超过给定的 max_w 和 max_h
        '''
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
        '''
        对图片进行处理，并限制窗口大小
        '''
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
        print('缩放尺寸：', img.size)
        return img

    def set_button(self):
        '''
        定义两个按钮
        '''
        self.btn_frame = Frame(self) 
        copy_bth = Button(self.btn_frame, text="复制结果", cursor='hand2', width=10, command=self.copy)
        copy_bth.pack(side='left', padx=20, pady=10)

        cancel_bth = Button(self.btn_frame, text="取消", cursor='hand2', width=10, command=self.cancel)
        cancel_bth.pack(side='right', padx=20, pady=10)
        self.btn_frame.pack(side='bottom')

    def copy(self):
        txt = self.res_text.get("1.0", END)
        p.copy(txt)
        self.destroy()

    def cancel(self):
        self.destroy()

    def show(self, img, txt):
        '''
        显示
        '''
        w, h = img.size

        self.tkImage = ImageTk.PhotoImage(image=img)
        self.label = Label(self, image=self.tkImage)
        self.label.config(image=self.tkImage)
        self.res_text = ScrolledText(self, height=10, background='#ffffff', font=("微软雅黑", 11))
        self.res_text.insert(END, txt)

        aspect_ratio = self.screen_w / self.screen_h
        if w >= h * aspect_ratio:
            self.label.pack(side='top', padx=10, pady=10)
            self.res_text.pack(side='top', padx=10, pady=10, fill='both')
        else:
            self.label.pack(side='left', padx=10, pady=10)
            self.res_text.pack(side='right', padx=10, pady=10, fill='both')

def getRect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

if __name__ == '__main__':
    # img = Image.open("src\\latex2.png")
    # memory = ImageText(img, '今天是个好日子')
    ocr = MemoryOCR(XUEERSI_ACCOUNTS)
    while True:
        sleep(0.2)
        im = ImageGrab.grabclipboard()          # 获取剪切板
        
        if isinstance(im, Image.Image):         # 判断是否是图片
            print('原始尺寸：', im.size)
            bf = BytesIO()
            im.save(bf, 'png')
            b64img = quote(b64encode(bf.getvalue()))
            # res = ocr.ocr(b64img)
            try:
                res = ocr.ocr(b64img)
                if isinstance(res, str):
                    text = res
                else:
                    text = '\n'.join(res['data']['content'])
                    rects = res['data']['recognition']['textLinePosition']
                    draw = ImageDraw.Draw(im)
                    for rect in rects:
                        draw.polygon(getRect(*rect), outline=(255,0,0))
            except Exception as e:
                text = str(e)
            
            # text = '我曾经跨过山和大海，也穿过人山人海'
            p.copy('')
            ImageText(im, text)
