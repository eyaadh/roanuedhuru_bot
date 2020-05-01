import time
from better_profanity import profanity
from roanu.utils.common import RoanuCommon
from pyrogram import Client, Message, Filters, Emoji, ChatPermissions

swear_jar_counter = []


@Client.on_message(Filters.chat(RoanuCommon.roanu_butler_chat), group=2)
async def swear_jar_resp(c: Client, m: Message):
    global swear_jar_counter

    chat_admins = await c.get_chat_members(chat_id=m.chat.id, filter='administrators')
    chat_admins_list = [x['user']['id'] for x in chat_admins]

    if m.from_user.id not in chat_admins_list and not m.service:
        mention = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
        if profanity.contains_profanity(m.text.encode('utf-8')):
            swear_jar_counter.append(m.from_user.id)
            swear_count = swear_jar_counter.count(m.from_user.id)
            if 3 <= swear_count < 6:
                owe_value = swear_count * 10
                await m.reply(
                    text=f"Hey {mention}! I guess you need to consider that you are at <b>a public chat</b> i.e. "
                         f"talk with some respect! \nYou owe {Emoji.MONEY_WITH_WINGS} <i>${owe_value}</i> "
                         f"{Emoji.MONEY_WITH_WINGS} to Swearjar now. \n<i>Once you reach <b>$60</b> you will be "
                         f"restricted for a day from sending messages within this chat.</i>",
                    parse_mode="html"
                )
            elif swear_count == 6:
                swear_jar_counter = [x for x in swear_jar_counter if x != m.from_user.id]
                await c.restrict_chat_member(chat_id=m.chat.id,
                                             user_id=m.from_user.id,
                                             permissions= ChatPermissions(
                                                 can_send_messages=False),
                                             until_date=int(time.time()+86400))
                await m.reply_text(
                    text=f"{Emoji.EXPLODING_HEAD} Ok that is enough {mention}! Now be restricted for "
                         f"the next {Emoji.ALARM_CLOCK} 24HRS."
                )
