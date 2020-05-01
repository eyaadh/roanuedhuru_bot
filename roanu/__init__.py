import logging
from pyrogram import Client
from roanu.utils.common import RoanuCommon

"""
 Configuration for the logger
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger(__name__)

roanuedhuru = Client(
        session_name=RoanuCommon.roanu_session,
        bot_token=RoanuCommon.roanu_api_key,
        workers=RoanuCommon.roanu_workers,
        workdir=RoanuCommon.roanu_working_dir,
        config_file=RoanuCommon.roanu_config_file
    )
