import os
import secrets
import logging
from gtts import gTTS
from tesserocr import PyTessBaseAPI, PSM
from pyrogram.errors import MessageEmpty
from roanu.utils.common import RoanuCommon
from pyrogram import Client, Message, Filters, Emoji


@Client.on_message(Filters.command(commands=['ocr'], prefixes=['/', '!']))
async def ocr_cmd(c: Client, m: Message):
    await m.reply_text(
        text="OCR: Kindly send me the Image from which you wish to extract text.\n<i>(As a reply to this message)</i>"
    )


@Client.on_message(Filters.photo & Filters.reply)
async def ocr_photo(c: Client, m: Message):
    if m.reply_to_message.text.partition(" ")[0] == "OCR:" \
            and m.reply_to_message.from_user.id == RoanuCommon.roanu_user_id:
        img = f"roanu/working_dir/{secrets.token_hex(4)}.jpg"
        await c.download_media(m, file_name=img)

        with PyTessBaseAPI(path="roanu/working_dir/tessaract", psm=PSM.AUTO_OSD, lang='eng+Thaana2') as api:
            api.SetImageFile(img)
            ocr_extracted = api.GetUTF8Text()

        try:
            await m.reply_text(
                text=ocr_extracted
            )

            voice = f"roanu/working_dir/{secrets.token_hex(4)}.mp3"
            if len(ocr_extracted) > 0:
                speech = gTTS(text=str(ocr_extracted), lang='en', slow=False)
                speech.save(voice)

                await m.reply_audio(
                    audio=voice
                )

            if os.path.exists(img):
                os.remove(img)

            if os.path.exists(voice):
                os.remove(voice)
        except MessageEmpty as e:
            await m.reply_text(
                text=f"Unfortunately, I could not read the image. This could be since we have not trained the tesseract "
                     f"enough {Emoji.MAN_SHRUGGING_DARK_SKIN_TONE}, remember this is just a DEMO."
            )
        except Exception as e:
            logging.error(str(e))
