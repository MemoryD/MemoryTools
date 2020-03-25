from time import time
from boxes import LabelBox
from setting import *
from utils import *

class Alert(object):
    def __init__(self, root, wt=90):
        self.root = root
        self.alert_time = wt
        self.is_alert = True
        self.start_time = time()

    def setConfig(self, config):
        if 'is_alert' in config:
            self.is_alert = config['is_alert']
        if 'alert_time' in config:
            self.alert_time = config['alert_time']

    def getConfig(self):
        config = {
            'is_alert': self.is_alert,
            'alert_time': self.alert_time
        }
        return config

    def createMenu(self):
        menu_options =  (
                            ("开启提醒", isCheckIcon(self.is_alert), self.pauseAlert),
                            ('30分钟', isPickIcon(self.alert_time == 30), self.changeTime30),
                            ('60分钟', isPickIcon(self.alert_time == 60), self.changeTime60),
                            ('90分钟', isPickIcon(self.alert_time == 90), self.changeTime90),
                            ('120分钟', isPickIcon(self.alert_time == 120), self.changeTime120),
                        )

        return menu_options

    def alert(self):
        minute = (time() - self.start_time) / 60       # 分钟数
        if minute >= self.alert_time:
            return True
        return False

    def alertText(self):
        return "关闭提醒" if self.is_alert else "开启提醒"

    def pauseAlert(self, sysTrayIcon):
        self.is_alert = not self.is_alert
        if self.is_alert:
            self.start_time = time()
        else:
            LabelBox().show("虽然你关掉了休息提醒，但还是要注意身体！", '确认')
        self.root.refreshMenu()

    def changeTime30(self, sysTrayIcon):
        self.alert_time = 30
        self.root.refreshMenu()
    
    def changeTime60(self, sysTrayIcon):
        self.alert_time = 60
        self.root.refreshMenu()

    def changeTime90(self, sysTrayIcon):
        self.alert_time = 90
        self.root.refreshMenu()
    
    def changeTime120(self, sysTrayIcon):
        self.alert_time = 120
        self.root.refreshMenu()

    def start(self):
        if self.is_alert and self.alert():                          # 是否到达预设的提醒时间
            alert_message = "你已经连续工作 %d 分钟了！是时候休息一下了！\n%s" % (self.alert_time, ALERT_MSG)
            LabelBox('危险警报').show(alert_message, '等你想要继续工作了再点我')
            self.start_time = time()
