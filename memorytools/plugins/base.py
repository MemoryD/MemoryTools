from easydict import EasyDict
from utils import getSrc


class BasePlugin(object):
    def __init__(self, name: str, root, icon: str, config: EasyDict):
        self.name = name
        self.root = root
        self.icon = icon
        self.config = config[name]

    def getConfig(self) -> EasyDict:
        return self.name, self.config

    def createMenu(self) -> tuple:
        return ()

    def initMenu(self) -> tuple:
        return self.name, getSrc(self.icon), self.createMenu(), True
