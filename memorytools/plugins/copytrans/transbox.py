# -*- coding: utf-8 -*-
"""
@file: basebox
@author: Memory
@date: 2020/10/11
@description: 复制翻译的弹出框
"""
from tkinter.scrolledtext import ScrolledText
from tools.basebox import BaseBox, END
from tools.utils import get_text_line


class TransBox(BaseBox):
    def __init__(self, title="翻译结果", copy_trans=None):
        buttons = [('重新翻译', self.retrans), ('复制', self.copy)]
        super(TransBox, self).__init__(buttons, title)
        self.copy_trans = copy_trans

    def set_text(self, textbox, text):
        textbox.delete("1.0", END)
        textbox.insert(END, text)

    def retrans(self):
        """
        根据用户的更改重新进行翻译
        """
        sentence = self.src_text.get("1.0", END)
        sentence = self.copy_trans.remove_newline(sentence)

        self.set_text(self.src_text, sentence)
        self.set_text(self.textbox, "翻译中，请稍候...")

        text = self.copy_trans.trans_text(sentence)
        self.set_text(self.textbox, text)

    def show(self, src: str, dest: str):
        h1 = min(10, max(5, get_text_line(src) + 1))
        h2 = min(10, max(5, get_text_line(dest) + 1))

        self.src_text = ScrolledText(self, height=h1, background='#ffffff', font=("微软雅黑", 11))
        self.textbox = ScrolledText(self, height=h2, background='#ffffff', font=("微软雅黑", 11))

        self.src_text.insert(END, str(src))
        self.src_text.config()
        self.textbox.insert(END, str(dest))

        self.src_text.pack(side='top', padx=10, pady=10)
        self.textbox.pack(side='top', padx=10, pady=10)

        self.start()
