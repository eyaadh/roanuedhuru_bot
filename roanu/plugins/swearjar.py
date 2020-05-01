from better_profanity import profanity
from pyrogram import Client, Message, Filters
from roanu import swear_jar_counter


@Client.on_message(Filters.chat("CityofAddu"))
async def swear_jar_resp(c: Client, m: Message):
    if profanity.contains_profanity(m.text):
        swear_jar_counter.append(m.from_user.id)
        if swear_jar_resp.count(m.from_user.id) > 3:
            await m.reply(
                text="Hey mind your language!"
            )
