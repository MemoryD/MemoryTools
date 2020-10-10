# -*- coding: utf-8 -*-

from pathlib import Path
from .transbox import TransBox
from googletransx import Translator
from tools.utils import is_check, is_pick, judge_language, paste_clip, copy_clip
from tools.logger import logger
from requests.exceptions import ConnectionError
from plugins import BasePlugin, change_config
from globals import ICON


class CopyTrans(BasePlugin):
    """
    一个复制翻译的插件，调用谷歌翻译的接口翻译剪切板中的文本
    """
    def __init__(self, root) -> None:
        config_path = Path(__file__).parent / "config.json"
        super(CopyTrans, self).__init__("复制翻译", root, ICON.trans, config_path)
        self.last = ''      # 记录上次的剪切板内容
        self.translator = self.get_translator()     # 获得翻译接口

    def create_menu(self) -> tuple:
        menu_options = (
            ("开启翻译", is_check(self.is_trans), self.pause_trans, True),
            ('去除换行', is_check(not self.newline), self.turn_newline, True),
            ('严格模式', is_check(self.strict), self.turn_strict, True),
            ('英文 <-> 中文', is_pick(self.mode == 'both'), self.both_mode, False),
            ('英文 --> 中文', is_pick(self.mode == 'en2zh'), self.en2zh_mode, False),
            ('中文 --> 英文', is_pick(self.mode == 'zh2en'), self.zh2en_mode, False),
        )

        return menu_options

    @classmethod
    def get_translator(cls):
        return Translator(service_urls=['translate.google.cn'])

    @change_config
    def pause_trans(self, s):
        self.is_trans = not self.is_trans
        if self.is_trans:
            logger.info("[复制翻译] 开启复制翻译")
        else:
            logger.info("[复制翻译] 关闭复制翻译")

    @change_config
    def en2zh_mode(self, s):
        self.mode = 'en2zh'
        self.src, self.dest = 'en', 'zh-cn'
        logger.info("[复制翻译] 切换翻译模式为: 英译中")

    @change_config
    def zh2en_mode(self, s):
        self.mode = 'zh2en'
        self.src, self.dest = 'zh-cn', 'en'
        logger.info("[复制翻译] 切换翻译模式为: 中译英")

    @change_config
    def both_mode(self, s):
        self.mode = 'both'
        logger.info("[复制翻译] 切换翻译模式为: 中英互译")

    @change_config
    def turn_strict(self, s):
        self.strict = not self.strict
        if self.strict:
            logger.info("[复制翻译] 开启严格模式")
        else:
            logger.info("[复制翻译] 关闭严格模式")

    @change_config
    def turn_newline(self, s):
        self.newline = not self.newline
        if not self.newline:
            logger.info("[复制翻译] 开启去除换行")
        else:
            logger.info("[复制翻译] 关闭去除换行")

    def remove_newline(self, source):
        if not self.newline:
            sentence = source.replace("\r", '').replace("\n", " ")
        else:
            sentence = source

        return sentence

    def pre_process(self, source):
        '''
        对剪切板的文本进行预处理。
        首先判断是否为空或者与上次复制的一致，如果是则不翻译。
        然后检测语言，是否不包含中英文，如果是则不翻译。
        再判断是否其中的目标语言占比过大，如果是则不翻译。
        如果是互译模式，根据检测结果设置源语言和目标语言。
        再判断是否要去除其中的换行。
        '''
        # 判断是否为空或与之前的内容一致
        if source == "" or source == self.last:
            return None
        # 去除文本两端的空格
        text = source.strip()
        logger.info("[复制翻译] 剪切板文本为: %s" % text)
        # 检测文本的语言
        src_language, score = judge_language(text)
        msg = "[复制翻译] 文本的主要语言为: %s, 占比: %s" % (src_language, score)
        logger.info(msg)
        # 文本中不含中英文则不翻译
        if not src_language:
            self.last = source
            logger.info("[复制翻译] 文本中不含中英文，因此不翻译.")
            return None
        # 文本中目标语言的占比过大则不翻译
        if self.mode != 'both' and src_language == self.dest and score > 0.8:
            logger.info("[复制翻译] 文本中目标语言的占比过大，因此不翻译.")
            self.last = source
            return None
        # 如果是中英互译，则根据检测的语言设置源语言和目标语言
        if self.mode == 'both':
            self.src = src_language
            self.dest = 'en' if src_language == 'zh-cn' else 'zh-cn'
        # 去除换行符
        sentence = self.remove_newline(text)

        return sentence

    def trans_text(self, sentence: str):
        """
        使用接口翻译文本，由于可能会失败，因此这里会重连三次
        :param sentence: 待翻译的文本
        :return: 翻译后的文本
        """
        text = sentence
        for i in range(3):
            try:
                if self.strict:
                    text = self.translator.translate(sentence, src=self.src, dest=self.dest).text
                else:
                    text = self.translator.translate(sentence, dest=self.dest).text
                return text
            except ConnectionError as ce:
                logger.error("[复制翻译] 连接失败: %s" % ce)
                self.translator = self.get_translator()
                text = str(ce)
            except Exception as e:
                logger.error("[复制翻译] 翻译出错: %s" % e)
                text = str(e)
        return text

    def trans(self, source: str):
        """
        对文本进行处理，看是否需要翻译，若否则不处理，若是则调用接口进行翻译并进行显示
        :param source: 待处理的文本
        :return:
        """
        sentence = self.pre_process(source)
        if not sentence:
            return None

        text = self.trans_text(sentence)

        if text == sentence:
            self.last = source
            logger.info('[复制翻译] 译文与原文一致，因此不显示。')
            return None
        logger.info('[复制翻译] 翻译结果为: %s' % text)
        TransBox(copy_trans=self).show(sentence, text)
        paste = paste_clip()
        if paste == source:
            copy_clip(sentence)
        self.last = paste_clip()

    def start(self):
        if not self.is_trans:  # 是否暂停
            return
        source = paste_clip()  # 获得剪切板内容
        self.trans(source)
