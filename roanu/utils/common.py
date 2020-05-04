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
        self.roanu_butler_chat = self.config.get("bot-configuration", "butler_chat")
        self.roanu_user_id = int(self.config.get("bot-configuration", "bot_user_id"))

        self.db_name = self.config.get("db", "db_name")
        self.db_username = self.config.get("db", "username")
        self.db_password = self.config.get("db", "password")
        self.db_host_address = self.config.get("db", "host_address")


RoanuCommon = Common()
