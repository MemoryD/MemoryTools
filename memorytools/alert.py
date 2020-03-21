import time
import threading
import easygui as g
from setting import *

class Alert(object):
    def __init__(self, root, wt=90):
        self.root = root
        self.alert_time = wt
        self.is_alert = True
        self.start_time = time.time()

    def alert(self):
        minute = (time.time() - self.start_time) / 60       # 分钟数
        if minute >= self.alert_time:
            return True
        return False

    def alert_text(self):
        return "关闭提醒" if self.is_alert else "开启提醒"

    def pause_alert(self, sysTrayIcon):
        self.is_alert = not self.is_alert
        if self.is_alert:
            self.start_time = time.time()
        else:
            g.msgbox("虽然你关掉了休息提醒，但还是要注意身体！")
        self.root.create_menu()
        sysTrayIcon.refresh_menu(self.root.menu_options)

    def change_time(self, sysTrayIcon):
        minute = g.integerbox("请输入提醒时间，即隔多少分钟提醒您该休息。\n"+ALERT_MSG, default=self.alert_time, lowerbound=1, upperbound=150)
        if minute is not None:
            self.alert_time = minute

    def start(self):
        while True:
            if self.is_alert and self.alert():                          # 是否到达预设的提醒时间
                alert_message = "你已经连续工作 %d 分钟了！是时候休息一下了！\n%s" % (self.alert_time, ALERT_MSG)
                g.msgbox(alert_message, ok_button="等你想要继续工作了再点我")
                self.start_time = time.time()                           # 重置开始时间
            time.sleep(0.2)                                             # 隔 0.1s 检测一次

    def run(self):
        thread = threading.Thread(target=self.start)
        thread.setDaemon(True)
        thread.start()