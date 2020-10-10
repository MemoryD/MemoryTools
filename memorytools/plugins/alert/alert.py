from time import time
from easydict import EasyDict
from tools.boxes import LabelBox
from globals import TEXT, ICON
from tools.utils import isCheckIcon, isPickIcon
from plugins import BasePlugin
from pathlib import Path


class Alert(BasePlugin):
    def __init__(self, root) -> None:
        config_path = Path(__file__).parent / "config.json"
        super(Alert, self).__init__("休息提醒", root, ICON.alert,  config_path)
        self.start_time = time()

    def create_menu(self):
        menu_options = (
                        ("开启提醒", isCheckIcon(self.is_alert), self.pauseAlert, True),
                        ('30分钟', isPickIcon(self.alert_time == 30), self.changeTime30, False),
                        ('60分钟', isPickIcon(self.alert_time == 60), self.changeTime60, False),
                        ('90分钟', isPickIcon(self.alert_time == 90), self.changeTime90, False),
                        ('120分钟', isPickIcon(self.alert_time == 120), self.changeTime120, False),
                        )

        return menu_options

    def alert(self):
        minute = (time() - self.start_time) / 60       # 分钟数
        if minute >= self.alert_time:
            return True
        return False

    def pauseAlert(self, s):
        self.is_alert = not self.is_alert
        if self.is_alert:
            self.start_time = time()
        else:
            print("虽然你关掉了休息提醒，但还是要注意身体！")
            # LabelBox().show("虽然你关掉了休息提醒，但还是要注意身体！", "确定")
        self.save_config()
        self.root.refreshMenu()

    def changeTime30(self, s):
        self.alert_time = 30
        self.save_config()
        self.root.refreshMenu()

    def changeTime60(self, s):
        self.alert_time = 60
        self.save_config()
        self.root.refreshMenu()

    def changeTime90(self, s):
        self.alert_time = 90
        self.save_config()
        self.root.refreshMenu()

    def changeTime120(self, s):
        self.alert_time = 120
        self.save_config()
        self.root.refreshMenu()

    def start(self):
        if self.is_alert and self.alert():
            alert_message = TEXT.alert % self.alert_time
            LabelBox('危险警报').show(alert_message, '等你想要继续工作了再点我')
            self.start_time = time()
