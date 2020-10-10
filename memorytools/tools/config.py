import json
from pathlib import Path
from easydict import EasyDict
from globals import PATH


class Configer(object):
    def __init__(self, path: Path, default=None):
        self.path = path
        self.default = default

    def readConfig(self) -> EasyDict:
        """
        读配置文件
        """
        if self.path.exists:
            config = self.path.read_text(encoding="utf-8")
        else:
            config = self.default
        return EasyDict(json.loads(config))

    def writeConfig(self, data: dict):
        """
        写配置文件
        """
        config = json.dumps(data, indent=4, ensure_ascii=False)
        self.path.write_text(config, encoding="utf-8")

