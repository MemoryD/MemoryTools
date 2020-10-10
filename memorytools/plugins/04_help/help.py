# -*- coding: utf-8 -*-
from os import startfile
from pathlib import Path
from webbrowser import open as open_web
from globals import ICON, PATH, URL
from plugins import BasePlugin


class Help(BasePlugin):
    def __init__(self, root) -> None:
        config_path = Path(__file__).parent / "config.json"
        super(Help, self).__init__("帮助", root, ICON.about, config_path)

    def about(self, s):
        """
        菜单中的 关于 选项
        """
        open_web(URL.github)

    def check_update(self, s):
        open_web(URL.release)

    def open_log(self, s):
        startfile(PATH.log.absolute())

    def create_menu(self) -> tuple:
        menu_options = (
            ("关于", None, self.about, True),
            ("日志", None, self.open_log, True),
            ("更新", None, self.check_update, True),
        )

        return menu_options

    def start(self) -> None:
        pass
