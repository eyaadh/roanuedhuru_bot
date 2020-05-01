from better_profanity import profanity
from pyrogram import Client, Message, Filters


@Client.on_message(Filters.chat("CityofAddu"))
async def swear_jar_resp(c: Client, m: Message):
    if profanity.contains_profanity(m.text):
        await m.reply(
            text="Hey mind your language!"
        )
