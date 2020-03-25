from time import time
from easygui import msgbox, integerbox
from setting import *

class Alert(object):
    def __init__(self, root, wt=90):
        self.root = root
        self.alert_time = wt
        self.is_alert = True
        self.start_time = time()

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
            msgbox("虽然你关掉了休息提醒，但还是要注意身体！")
        self.root.createMenu()
        sysTrayIcon.refreshMenu(self.root.menu_options)

    def changeTime(self, sysTrayIcon):
        minute = integerbox("请输入提醒时间，即隔多少分钟提醒您该休息。\n"+ALERT_MSG, default=self.alert_time, lowerbound=1, upperbound=150)
        if minute is not None:
            self.alert_time = minute

    def start(self):
        if self.is_alert and self.alert():                          # 是否到达预设的提醒时间
            alert_message = "你已经连续工作 %d 分钟了！是时候休息一下了！\n%s" % (self.alert_time, ALERT_MSG)
            msgbox(alert_message, ok_button="等你想要继续工作了再点我")
            self.start_time = time()