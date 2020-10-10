from pathlib import Path

from easydict import EasyDict

from tools.boxes import TextTextBox
from googletransx import Translator
from tools.utils import isCheckIcon, isPickIcon, judgeLanguage, pasteClip
from requests.exceptions import ConnectionError
from plugins import BasePlugin
from globals import ICON


class CopyTrans(BasePlugin):
    def __init__(self, root) -> None:
        config_path = Path(__file__).parent / "config.json"
        super(CopyTrans, self).__init__("复制翻译", root, ICON.trans, config_path)
        self.last = ''  # 记录上次的剪切板内容
        self.translator = Translator(service_urls=['translate.google.cn'])  # 获得翻译接口

    def create_menu(self) -> tuple:
        menu_options = (
            ("开启翻译", isCheckIcon(self.is_trans), self.pauseTrans, True),
            ('去除换行', isCheckIcon(not self.newline), self.turnNewline, True),
            ('严格模式', isCheckIcon(self.strict), self.turnStrict, True),
            ('英文 <-> 中文', isPickIcon(self.mode == 'both'), self.bothMode, False),
            ('英文 --> 中文', isPickIcon(self.mode == 'en2zh'), self.en2zhMode, False),
            ('中文 --> 英文', isPickIcon(self.mode == 'zh2en'), self.zh2enMode, False),
        )

        return menu_options

    def pauseTrans(self, sysTrayIcon):
        self.is_trans = not self.is_trans
        self.save_config()
        self.root.refreshMenu()

    def en2zhMode(self, sysTrayIcon):
        self.mode = 'en2zh'
        self.src, self.dest = 'en', 'zh-cn'
        self.save_config()
        self.root.refreshMenu()

    def zh2enMode(self, sysTrayIcon):
        self.mode = 'zh2en'
        self.src, self.dest = 'zh-cn', 'en'
        self.save_config()
        self.root.refreshMenu()

    def bothMode(self, sysTrayIcon):
        self.mode = 'both'
        self.save_config()
        self.root.refreshMenu()

    def turnStrict(self, sysTrayIcon):
        self.strict = not self.strict
        self.save_config()
        self.root.refreshMenu()

    def turnNewline(self, sysTrayIcon):
        self.newline = not self.newline
        self.save_config()
        self.root.refreshMenu()

    def removeNewline(self, source):
        if not self.newline:
            sentence = source.replace("\r", '').replace("\n", " ")
        else:
            sentence = source

        return sentence

    def preProcess(self, source):
        '''
        对剪切板的文本进行预处理。
        首先判断是否为空或者与上次复制的一致，如果是则不翻译。
        然后检测语言，是否不包含中英文，如果是则不翻译。
        再判断是否其中的目标语言占比过大，如果是则不翻译。
        如果是互译模式，根据检测结果设置源语言和目标语言。
        再判断是否要去除其中的换行。
        '''
        if source == "" or source == self.last:
            return None
        text = source.strip()
        src_language, score = judgeLanguage(text)
        print('检测为：%s, %s. 目标语言为：%s' % (src_language, score, self.dest))
        if not src_language:
            self.last = source
            return None
        if self.mode != 'both' and src_language == self.dest and score > 0.8:
            self.last = source
            return None

        if self.mode == 'both':
            self.src = src_language
            self.dest = 'en' if src_language == 'zh-cn' else 'zh-cn'

        sentence = self.removeNewline(text)

        return sentence

    def transText(self, sentence: str):
        for i in range(3):
            try:
                if self.strict:
                    text = self.translator.translate(sentence, src=self.src, dest=self.dest).text
                else:
                    text = self.translator.translate(sentence, dest=self.dest).text
                return text
            except ConnectionError as ce:
                print(ce)
                self.translator = Translator(service_urls=['translate.google.cn'])
                text = str(ce)
            except Exception as e:
                print(e)
                text = str(e)
        return text

    def trans(self, source: str):
        sentence = self.preProcess(source)
        if not sentence:
            return None

        text = self.transText(sentence)

        if text == sentence:
            self.last = source
            print('译文与原文一致，因此不显示。')
            return None
        # print("%s\n%s\n" % (sentence, text))
        TextTextBox('翻译结果').show(sentence, text)
        # paste = pasteClip()
        # if paste == source:
        #     copyClip(sentence)
        self.last = pasteClip()

    def start(self):
        if not self.is_trans:  # 是否暂停
            return
        source = pasteClip()  # 获得剪切板内容
        self.trans(source)
