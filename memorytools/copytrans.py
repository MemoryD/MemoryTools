#!python3
# -*- coding:utf-8 -*-

import pyperclip as p
from boxes import TextTextBox
from googletransx import Translator
from utils import *


class CopyTrans(object):
    def __init__(self, root):
        self.root = root
        self.is_pause = False
        self.src = 'en'
        self.dest = 'zh-cn'
        self.strict_mode = False
        self.newline = False
        self.last = ''                                                  # 记录上次的剪切板内容
        self.translator = Translator(service_urls=['translate.google.cn'])   # 获得翻译接口

    def setConfig(self, config):
        if 'mode' in config:
            pass

    def turnLanguage(self, sysTrayIcon):
        self.src, self.dest = self.dest, self.src
        self.last = ''
        self.root.createMenu()
        sysTrayIcon.refreshMenu(self.root.menu_options)

    def trans(self, translator, source):
        if source == "" or source == self.last:                         # 是否为空或者跟上次一样
            return None

        la = judgeLanguage(source)
        print(la, self.dest)
        if la == self.dest:                         # 是否为纯目标语言
            self.last = source
            return None

        if not self.newline:
            sentence = source.replace("\r", '').replace("\n", " ")          # 去除换行符
        else:
            sentence = source

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
        TextTextBox('翻译结果').show(sentence, text)
        self.last = p.paste()

    def start(self):
        if self.is_pause:                                           # 是否暂停
            return
        source = p.paste()                                          # 获得剪切板内容
        self.trans(self.translator, source)

    def pauseTrans(self, sysTrayIcon):
        self.is_pause = not self.is_pause
        self.root.createMenu()
        sysTrayIcon.refreshMenu(self.root.menu_options)

    def turnStrict(self, sysTrayIcon):
        self.strict_mode = not self.strict_mode
        self.root.createMenu()
        sysTrayIcon.refreshMenu(self.root.menu_options)

    def turnNewline(self, sysTrayIcon):
        self.newline = not self.newline
        self.root.createMenu()
        sysTrayIcon.refreshMenu(self.root.menu_options)

    def pauseText(self):
        return "开启翻译" if self.is_pause else "暂停翻译"

    def languageText(self):
        if self.dest == 'zh-cn':
            return '英文 --> 中文'
        else:
            return '中文 --> 英文'

    def newlineText(self):
        return "去除换行：否" if self.newline else "去除换行：是"

    def strictText(self):
        return "关闭严格模式" if self.strict_mode else "开启严格模式"
