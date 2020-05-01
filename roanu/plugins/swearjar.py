import time
import logging
from roanu import roanuedhuru
from better_profanity import profanity
from roanu.utils.common import RoanuCommon
from pyrogram import Client, Message, Filters, Emoji, ChatPermissions
from pyrogram.errors import UserIdInvalid, UsernameNotOccupied, PeerIdInvalid

swear_jar_counter = []


@Client.on_message(Filters.chat(RoanuCommon.roanu_butler_chat), group=2)
async def swear_jar_resp(c: Client, m: Message):
    global swear_jar_counter

    chat_admins = await c.get_chat_members(chat_id=m.chat.id, filter='administrators')
    chat_admins_list = [x['user']['id'] for x in chat_admins]

    if m.from_user.id not in chat_admins_list and not m.service:
        mention = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
        try:
            if profanity.contains_profanity(m.text.encode('ascii', 'ignore').decode('ascii')):
                swear_jar_counter.append(m.from_user.id)
                swear_count = swear_jar_counter.count(m.from_user.id)
                if 3 <= swear_count < 6:
                    owe_value = swear_count * 10
                    await m.reply(
                        text=f"Hey {mention}! I guess you need to consider that you are at <b>a public chat</b> i.e. "
                             f"talk with some respect! \nYou owe {Emoji.MONEY_WITH_WINGS} <i>${owe_value}</i> "
                             f"{Emoji.MONEY_WITH_WINGS} to SwearJar now. \n<i>Once you reach <b>$60</b> you will be "
                             f"restricted for a day from sending messages within this chat.</i>",
                        parse_mode="html"
                    )
                elif swear_count == 6:
                    swear_jar_counter = [x for x in swear_jar_counter if x != m.from_user.id]
                    await c.restrict_chat_member(chat_id=m.chat.id,
                                                 user_id=m.from_user.id,
                                                 permissions=ChatPermissions(
                                                     can_send_messages=False),
                                                 until_date=int(time.time() + 86400))
                    await m.reply_text(
                        text=f"{Emoji.EXPLODING_HEAD} Ok that is enough {mention}! Now be restricted for "
                             f"the next {Emoji.ALARM_CLOCK} 24HRS."
                    )
        except Exception as e:
            logging.error(str(e))


@Client.on_message(Filters.command(commands=['rc'], prefixes=['/', '!']) & Filters.chat(RoanuCommon.roanu_butler_chat))
async def swear_jar_reset_counter(c: Client, m: Message):
    global swear_jar_counter

    chat_admins = await c.get_chat_members(chat_id=m.chat.id, filter='administrators')
    chat_admins_list = [x['user']['id'] for x in chat_admins]

    if m.from_user.id in chat_admins_list:
        split_input = m.text.split(" ")
        if len(split_input) == 2:
            try:
                if split_input[1].isdigit():
                    exp_user = await c.get_chat_member(
                        chat_id=RoanuCommon.roanu_butler_chat,
                        user_id=int(split_input[1])
                    )
                    await reset_counter(m.chat.id, exp_user.user.id)
                else:
                    if split_input[1][1] == "@":
                        exp_user = split_input[1][1:]
                        exp_user = await c.get_chat_member(
                            chat_id=RoanuCommon.roanu_butler_chat,
                            user_id=exp_user
                        )
                        await reset_counter(m.chat.id, exp_user.user.id)
                    else:
                        exp_user = await c.get_chat_member(
                            chat_id=RoanuCommon.roanu_butler_chat,
                            user_id=split_input[1]
                        )
                        await reset_counter(m.chat.id, exp_user.user.id)
            except (UserIdInvalid, UsernameNotOccupied, PeerIdInvalid) as e:
                await m.reply_text(
                    text=f"Seems that user is not present in this chat anymore. \n"
                         f"<b>Error:</b> <i>{str(e)}</i>"
                )
            except Exception as e:
                logging.error(str(e))


async def reset_counter(chat_id, user_id):
    global swear_jar_counter

    if user_id in swear_jar_counter:
        swear_jar_counter = [x for x in swear_jar_counter if x != user_id]
        await roanuedhuru.send_message(
            chat_id=chat_id,
            text="I have removed the user from my counter for SwearJar."
        )
    else:
        await m.reply_text(
            text="Well that user is not in the SwearJar List"
        )
