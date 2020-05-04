import json
import random
from PyDictionary import PyDictionary
from pyrogram import Client, Message, Filters, Emoji
from roanu.utils.database.crossword import RoanuCrossword


@Client.on_message(Filters.command(commands=['crossword'], prefixes=['/', '!']))
async def crossword_command(c: Client, m: Message):
    with open("roanu/working_dir/words.json") as f:
        words_raw = f.read()

    words = json.loads(words_raw)
    random_word = random.choice(words)

    dictionary = PyDictionary()

    list_random_word = list(random_word)
    shuffled_list_random_word = random.sample(list_random_word, len(list_random_word))

    shuffled_word = f" {Emoji.WHITE_SMALL_SQUARE} ".join(shuffled_list_random_word)
    rwm = dictionary.meaning(random_word)

    cross_msg = await m.reply_text(
        text=f"<b>CROSSWORD:</b> \nWell try make a word using all these letters "
             f"and reply to this message with the solved crossword.\n"
             f"<b>{Emoji.HEAVY_MINUS_SIGN} {shuffled_word} {Emoji.HEAVY_MINUS_SIGN}</b>\n"
             f"<b>Word Description:</b> \n<i>{rwm['Verb'][0] if 'Verb' in rwm else rwm['Noun'][0]}</i>",
        parse_mode="html"
    )

    await RoanuCrossword().insert_messages(
        chat_id=m.chat.id,
        message_id=cross_msg.message_id,
        word=random_word,
        shuffled=list_random_word
    )


@Client.on_message(Filters.reply, group=3)
async def crossword_reply(c: Client, m: Message):
    origin_message_document = await RoanuCrossword().find_message(
        chat_id=m.chat.id,
        message_id=m.reply_to_message.message_id
    )

    if origin_message_document:
        word = origin_message_document['word']
        if 'answered' not in origin_message_document:
            if m.text == word:
                await m.reply_text(
                    text=f"{Emoji.SPARKLES} That's correct! {Emoji.SPARKLES}",
                    reply_to_message_id=m.message_id
                )
                await RoanuCrossword().update_answer(
                    chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id
                )
            else:
                await m.reply_text(
                    text="That is not the word, may be try again?",
                    reply_to_message_id=m.message_id
                )
        else:
            await m.reply_text(
                text="That question has already been answered, try a new one may be?",
                reply_to_message_id=m.message_id
            )
