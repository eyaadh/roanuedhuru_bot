import asyncio
from pyrogram import Client
from roanu.utils.common import RoanuCommon
from better_profanity import profanity


async def main():
    roanu = Client(
        session_name=RoanuCommon.roanu_session,
        bot_token=RoanuCommon.roanu_api_key,
        workers=RoanuCommon.roanu_workers,
        workdir=RoanuCommon.roanu_working_dir,
        config_file=RoanuCommon.roanu_config_file
    )

    profanity.add_censor_words(['ngbl', 'nagoobalha', 'balha'])

    await roanu.start()
    await roanu.idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
