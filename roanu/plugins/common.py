from roanu.utils.common import RoanuCommon
from pyrogram import Client, Message, Filters, Emoji


@Client.on_message(Filters.new_chat_members & Filters.chat(RoanuCommon.roanu_butler_chat), group=1)
async def new_chat_members(c: Client, m: Message):
    mentions = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
    welcome_msg = "{} Welcome to <a href='https://t.me/CityofAddu'>AdduCity Group</a>'s group chat! Keep your " \
                  "calm and enjoy the chat."

    new_members = [mentions.format(i.first_name, i.id) for i in m.new_chat_members]
    text = welcome_msg.format(Emoji.MAN_RAISING_HAND_DARK_SKIN_TONE, ", ".join(new_members))

    await m.reply_text(
        text=text,
        parse_mode="html",
        disable_web_page_preview=True
    )


@Client.on_message(Filters.command(commands=['start'], prefixes=['/', '!']))
async def start_handler(c: Client, m: Message):
    mention = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
    await m.reply_text(
        text=f"Hello {mention}! I am the butler build for {RoanuCommon.roanu_butler_chat}, a simple & sweet Open-source"
             f" telegram bot. \nSource Code can be found <a href='https://github.com/eyaadh/roanuedhuru_bot'>here."
             f"</a>",
        parse_mode="html",
        disable_web_page_preview=True
    )


@Client.on_message(Filters.command(commands=['help'], prefixes=['/', '!']))
async def help_handler(c: Client, m: Message):
    await m.reply_text(
        text=f"I am the butler build for {RoanuCommon.roanu_butler_chat}, a simple & sweet Open-source telegram bot. \n"
             f"Source Code can be found <a href='https://github.com/eyaadh/roanuedhuru_bot'>here.</a>",
        parse_mode="html",
        disable_web_page_preview=True
    )
