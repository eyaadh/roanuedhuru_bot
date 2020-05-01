import configparser
from pathlib import Path


class Common:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.roanu_working_dir = Path("roanu/working_dir/")
        self.roanu_config_file = Path("roanu/working_dir/config.ini")
        self.config.read(self.roanu_config_file)

        self.roanu_session = self.config.get("bot-configuration", "session_name")
        self.roanu_api_key = self.config.get("bot-configuration", "api_key")
        self.roanu_workers = int(self.config.get("bot-configuration", "workers"))


RoanuCommon = Common()
