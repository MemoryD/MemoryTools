import json
from easydict import EasyDict
from globals import PATH


class Config(object):
    def __init__(self, path=PATH.config):
        self.path = path

    def readConfig(self) -> EasyDict:
        """
        读配置文件
        """
        config = self.path.read_text(encoding="utf-8")
        return EasyDict(json.loads(config))

    def writeConfig(self, data: dict):
        """
        写配置文件
        """
        config = json.dumps(data, indent=4, ensure_ascii=False)
        self.path.write_text(config, encoding="utf-8")

