import pymongo
from roanu.utils.common import RoanuCommon


class RoanuDB:
    def __init__(self):
        self.db_client = pymongo.MongoClient(
            f"mongodb://"
            f"{RoanuCommon.db_username}:{RoanuCommon.db_password}@{RoanuCommon.db_host_address}"
        )
        self.db = self.db_client[f"{RoanuCommon.db_name}"]
