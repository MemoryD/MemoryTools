# -*- coding: utf-8 -*-
from time import time
from .alertbox import AlertBox
from globals import TEXT, ICON
from tools.utils import is_check, is_pick
from tools.logger import logger
from plugins import BasePlugin, change_config
from pathlib import Path


class Alert(BasePlugin):
    def __init__(self, root) -> None:
        config_path = Path(__file__).parent / "config.json"
        super(Alert, self).__init__("休息提醒", root, ICON.alert,  config_path)
        self.start_time = time()

    def create_menu(self):
        menu_options = (
                        ("开启提醒", is_check(self.is_alert), self.pause_alert, True),
                        ('30分钟', is_pick(self.alert_time == 30), self.set_alert_time_30, False),
                        ('60分钟', is_pick(self.alert_time == 60), self.set_alert_time_60, False),
                        ('90分钟', is_pick(self.alert_time == 90), self.set_alert_time_90, False),
                        ('120分钟', is_pick(self.alert_time == 120), self.set_alert_time_120, False),
                        )

        return menu_options

    @change_config
    def pause_alert(self, s):
        self.is_alert = not self.is_alert
        if self.is_alert:
            self.start_time = time()
            logger.info("[休息提醒] 开启休息提醒")
        else:
            logger.info("[休息提醒] 关闭休息提醒")
            # LabelBox().show("虽然你关掉了休息提醒，但还是要注意身体！", "确定")

    @change_config
    def set_alert_time_30(self, s):
        self.alert_time = 30
        logger.info("[休息提醒] 将休息提醒时间设置为 30 分钟.")

    @change_config
    def set_alert_time_60(self, s):
        self.alert_time = 60
        logger.info("[休息提醒] 将休息提醒时间设置为 60 分钟.")

    @change_config
    def set_alert_time_90(self, s):
        self.alert_time = 90
        logger.info("[休息提醒] 将休息提醒时间设置为 90 分钟.")

    @change_config
    def set_alert_time_120(self, s):
        self.alert_time = 120
        logger.info("[休息提醒] 将休息提醒时间设置为 120 分钟.")

    def alert(self):
        minute = (time() - self.start_time) / 60       # 分钟数
        if minute >= self.alert_time:
            return True
        return False

    def start(self):
        if self.is_alert and self.alert():
            alert_message = TEXT.alert % self.alert_time
            AlertBox('危险警报').show(alert_message, '等你想要继续工作了再点我')
            self.start_time = time()

