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
        self.mode = 'both'
        self.src = 'en'
        self.dest = 'zh-cn'
        self.strict_mode = False
        self.newline = False
        self.last = ''                                                  # 记录上次的剪切板内容
        self.translator = Translator(service_urls=['translate.google.cn'])   # 获得翻译接口

    def createMenu(self):
        menu_options =  (
                            ("开启翻译", isCheckIcon(not self.is_pause), self.pauseTrans),
                            ('去除换行', isCheckIcon(not self.newline), self.turnNewline),
                            ('严格模式', isCheckIcon(self.strict_mode), self.turnStrict),
                            ('英文 <-> 中文', isPickIcon(self.mode=='both'), self.bothMode),
                            ('英文 --> 中文', isPickIcon(self.mode=='en2zh'), self.en2zhMode),
                            ('中文 --> 英文', isPickIcon(self.mode=='zh2en'), self.zh2enMode),
                        )

        return menu_options

    def pauseTrans(self, sysTrayIcon):
        self.is_pause = not self.is_pause
        self.root.refreshMenu()

    def en2zhMode(self, sysTrayIcon):
        self.mode = 'en2zh'
        self.src, self.dest = 'en', 'zh-cn'
        self.root.refreshMenu()

    def zh2enMode(self, sysTrayIcon):
        self.mode = 'zh2en'
        self.src, self.dest = 'zh-cn', 'en'
        self.root.refreshMenu()

    def bothMode(self, sysTrayIcon):
        self.mode = 'both'
        self.root.refreshMenu()

    def turnStrict(self, sysTrayIcon):
        self.strict_mode = not self.strict_mode
        self.root.refreshMenu()

    def turnNewline(self, sysTrayIcon):
        self.newline = not self.newline
        self.root.refreshMenu()

    def setConfig(self, config):
        if 'mode' in config:
            pass

    def trans(self, translator, source):
        if source == "" or source == self.last:                         # 是否为空或者跟上次一样
            return None

        la, pro = judgeLanguage(source)
        print('检测为：%s, %s. 目标语言为：%s'%(la, pro, self.dest))
        if self.mode != 'both' and la == self.dest and pro > 0.8:                         # 是否为纯目标语言
            self.last = source
            return None

        if not self.newline:
            sentence = source.replace("\r", '').replace("\n", " ")          # 去除换行符
        else:
            sentence = source

        if self.mode == 'both':
            self.src = la
            self.dest = 'en' if la == 'zh-cn' else 'zh-cn'

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
            print('译文与原文一致，因此不显示。')
            return None
        print("%s\n%s\n" % (sentence, text))                            # 打印到命令行
        TextTextBox('翻译结果').show(sentence, text)
        self.last = p.paste()

    def start(self):
        if self.is_pause:                                           # 是否暂停
            return
        source = p.paste()                                          # 获得剪切板内容
        self.trans(self.translator, source)
