from time import time

from easydict import EasyDict

from boxes import LabelBox
from setting import ALERT_MSG
from utils import isCheckIcon, isPickIcon


class Alert(object):
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.start_time = time()

    def getConfig(self) -> EasyDict:
        return self.config

    def createMenu(self):
        menu_options = (
                        ("开启提醒", isCheckIcon(self.config.is_alert), self.pauseAlert, True),
                        ('30分钟', isPickIcon(self.config.alert_time == 30), self.changeTime30, False),
                        ('60分钟', isPickIcon(self.config.alert_time == 60), self.changeTime60, False),
                        ('90分钟', isPickIcon(self.config.alert_time == 90), self.changeTime90, False),
                        ('120分钟', isPickIcon(self.config.alert_time == 120), self.changeTime120, False),
                        )

        return menu_options

    def alert(self):
        minute = (time() - self.start_time) / 60       # 分钟数
        if minute >= self.config.alert_time:
            return True
        return False

    def alertText(self):
        return "关闭提醒" if self.config.is_alert else "开启提醒"

    def pauseAlert(self, sysTrayIcon):
        self.config.is_alert = not self.config.is_alert
        if self.config.is_alert:
            self.start_time = time()
        else:
            LabelBox().show("虽然你关掉了休息提醒，但还是要注意身体！", '确认')
        self.root.refreshMenu()

    def changeTime30(self, sysTrayIcon):
        self.config.alert_time = 30
        self.root.refreshMenu()

    def changeTime60(self, sysTrayIcon):
        self.config.alert_time = 60
        self.root.refreshMenu()

    def changeTime90(self, sysTrayIcon):
        self.config.alert_time = 90
        self.root.refreshMenu()

    def changeTime120(self, sysTrayIcon):
        self.config.alert_time = 120
        self.root.refreshMenu()

    def start(self):
        if self.config.is_alert and self.alert():
            alert_message = "你已经连续工作 %d 分钟了！是时候休息一下了！\n%s" % (self.config.alert_time, ALERT_MSG)
            LabelBox('危险警报').show(alert_message, '等你想要继续工作了再点我')
            self.start_time = time()
