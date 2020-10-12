# -*- coding: utf-8 -*-
"""
@file: alert
@author: Memory
@date: 2020/10/11
@description: 用于工作提醒
"""
from time import time
from .alertbox import AlertBox
from globals import TEXT, ICON, PATH
from tools.utils import is_check, is_pick
from tools.logger import logger
from plugins import BasePlugin, change_config
from PIL import ImageGrab


class Alert(BasePlugin):
    def __init__(self, root) -> None:
        config_path = PATH.config / ("%s.json" % self.__class__.__name__)
        super(Alert, self).__init__("工作提醒", root, ICON.alert,  config_path)
        self.config = self.init_config()
        self.rest_start_time = time()

        self.slack_start_time = time()
        self.last_screen = ImageGrab.grab().getdata()
        self.check_interval = 10
        self.last_check_time = time()
        self.similarity_thresold = 0.96

    def create_menu(self):
        menu_options = (
                        ("休息提醒", is_check(self.is_rest_alert), self.pause_rest_alert, True),
                        ('30分钟', is_pick(self.rest_time == 30), self.set_rest_time, False),
                        ('60分钟', is_pick(self.rest_time == 60), self.set_rest_time, False),
                        ('90分钟', is_pick(self.rest_time == 90), self.set_rest_time, True),
                        ("摸鱼提醒", is_check(self.is_slack_alert), self.pause_slack_alert, True),
                        ('10分钟', is_pick(self.slack_time == 10), self.set_slack_time, False),
                        ('15分钟', is_pick(self.slack_time == 15), self.set_slack_time, False),
                        ('20分钟', is_pick(self.slack_time == 20), self.set_slack_time, False),
                        )

        return menu_options

    def create_default_config(self) -> dict:
        config = {
            "is_rest_alert": True,
            "rest_time": 60,
            "is_slack_alert": True,
            "slack_time": 15
        }
        return config

    @change_config
    def pause_rest_alert(self, option_text):
        self.is_rest_alert = not self.is_rest_alert
        if self.is_rest_alert:
            self.rest_start_time = time()
            logger.info("[休息提醒] 开启休息提醒")
        else:
            logger.info("[休息提醒] 关闭休息提醒")

    @change_config
    def pause_slack_alert(self, option_text):
        self.is_slack_alert = not self.is_slack_alert
        if self.is_slack_alert:
            self.slack_start_time = time()
            logger.info("[休息提醒] 开启摸鱼提醒")
        else:
            logger.info("[休息提醒] 关闭摸鱼提醒")

    @change_config
    def set_rest_time(self, option_text):
        self.rest_time = int(option_text[:2])
        logger.info("[休息提醒] 将休息提醒时间设置为 %d 分钟." % self.rest_time)

    @change_config
    def set_slack_time(self, option_text):
        self.slack_time = int(option_text[:2])
        logger.info("[休息提醒] 将摸鱼提醒时间设置为 %d 分钟." % self.slack_time)

    def alert(self):
        minute = (time() - self.rest_start_time) / 60       # 分钟数
        if minute >= self.rest_time:
            return True
        return False

    def slack(self):
        """
        判断是否在摸鱼
        首先，程序每隔 self.check_interval 秒钟检查一次屏幕，将其与上一次的屏幕进行对比，
        如果相似度超过 self.similarity_thresold, 则判断为摸鱼。
        如果摸鱼时间超过了 self.slack_time，那么将会弹窗提醒。
        """
        check = (time() - self.last_check_time) > self.check_interval
        if check:
            self.last_check_time = time()
            current_screen = ImageGrab.grab().getdata()
            similarity = 0
            for i, j in zip(current_screen, self.last_screen):
                if i == j:
                    similarity += 1
            similarity = similarity / len(current_screen)
            # print(similarity)
            self.last_screen = current_screen

            if similarity >= self.similarity_thresold:
                minute = (time() - self.slack_start_time) / 60
                # print(minute, self.slack_time)
                if minute >= self.slack_time:
                    return True
            else:
                self.slack_start_time = time()

        return False

    def start(self):
        if self.is_rest_alert and self.alert():
            alert_message = TEXT.rest_alert % self.rest_time
            AlertBox('危险警报').show(alert_message, '想要继续工作了再点我')
            self.rest_start_time = time()
            self.slack_start_time = time()

        if self.is_slack_alert and self.slack():
            alert_message = TEXT.slack_alert % self.slack_time
            AlertBox('摸鱼警报').show(alert_message, '点我开始工作')
            self.rest_start_time = time()
            self.slack_start_time = time()
