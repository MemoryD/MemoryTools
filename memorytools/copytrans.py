#!python3
# -*- coding:utf-8 -*-

import easygui as g
import pyperclip as p
from googletransx import Translator
from utils import *


class CopyTrans(object):
    def __init__(self, root):
        self.root = root
        self.is_pause = False
        self.src = 'en'
        self.dest = 'zh-cn'
        self.strict_mode = False
        self.last = ''                                                  # 记录上次的剪切板内容
        self.translator = Translator(service_urls=['translate.google.cn'])   # 获得翻译接口

    def turn_language(self, sysTrayIcon):
        self.src, self.dest = self.dest, self.src
        self.last = ''
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def trans(self, translator, source):
        if source == "" or source == self.last:                         # 是否为空或者跟上次一样
            return None

        la = judge_language(source)
        print(la, self.dest)
        if la == self.dest:                         # 是否为纯目标语言
            self.last = source
            return None

        sentence = source.replace("\r", '').replace("\n", " ")          # 去除换行符

        try:
            if self.strict_mode:
                text = translator.translate(sentence, src=self.src, dest=self.dest).text  # 翻译
            else:
                text = translator.translate(sentence, dest=self.dest).text
        except Exception as e:
            text = str(e)
        # 如果与原文本一样，则不显示
        if text == sentence:
            self.last = source
            return None
        print("%s\n%s\n" % (sentence, text))                            # 打印到命令行
        res = g.ccbox(text, choices=("复制", "取消"))                    # 显示翻译内容，及是否要复制
        if res == 1:                                                    # 按下了 复制 按钮
            p.copy(text)                                                # 复制到剪切板
            self.last = text
        else:
            p.copy(sentence)
            self.last = sentence

    def start(self):
        if self.is_pause:                                           # 是否暂停
            return
        source = p.paste()                                          # 获得剪切板内容
        self.trans(self.translator, source)

    def pause_trans(self, sysTrayIcon):
        self.is_pause = not self.is_pause
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def turn_strict(self, sysTrayIcon):
        self.strict_mode = not self.strict_mode
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def pause_text(self):
        return "开启翻译" if self.is_pause else "暂停翻译"

    def language_text(self):
        if self.dest == 'zh-cn':
            return '英文 --> 中文'
        else:
            return '中文 --> 英文'

    def strict_text(self):
        return "关闭严格模式" if self.strict_mode else "开启严格模式"
