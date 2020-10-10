import json
from easydict import EasyDict


class BasePlugin(object):
    def __init__(self, name: str, root, icon: str, config_path):
        self.name = name
        self.root = root
        self.icon = icon
        self.config_path = config_path
        self.config = self.init_config()

    def init_config(self):
        config = self.config_path.read_text(encoding="utf-8")
        config = EasyDict(json.loads(config))

        for attr, value in config.items():
            self.__setattr__(attr, value)

        return config

    def save_config(self):
        for attr in self.config:
            self.config[attr] = self.__getattribute__(attr)

        data = json.dumps(self.config, indent=4, ensure_ascii=False)
        self.config_path.write_text(data, encoding="utf-8")

    # def create_default_config(self) -> EasyDict:
    #     raise NotImplementedError

    def create_menu(self) -> tuple:
        return ()

    def init_menu(self) -> tuple:
        return self.name, self.icon, self.create_menu(), True

    def start(self):
        raise NotImplementedError
