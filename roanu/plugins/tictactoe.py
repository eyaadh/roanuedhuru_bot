import asyncio
import logging
from roanu.utils.database.ticktactoe import RoanuTicTacToe
from pyrogram import Client, Message, Filters, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Emoji
from pyrogram.errors import FloodWait


async def insert_play(letter, pos, board):
    board[pos] = letter


async def is_space_free(pos, board):
    return board[pos] == ' '


async def select_random(li):
    import random
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]


async def is_winner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal


async def roanu_move(board):
    move_possibilities = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]

    move = 0

    for let in ['✔️', '✖️']:
        for i in move_possibilities:
            board_copy = board[:]
            board_copy[i] = let
            if await is_winner(board_copy, let):
                move = i
                return move

    corners_open = []
    for i in move_possibilities:
        if i in [1, 3, 7, 9]:
            corners_open.append(i)

    if len(corners_open) > 0:
        move = await select_random(corners_open)
        return move

    if 5 in move_possibilities:
        move = 5
        return move

    edges_open = []
    for i in move_possibilities:
        if i in [2, 4, 6, 8]:
            edges_open.append(i)

    if len(edges_open) > 0:
        move = await select_random(edges_open)

    return move


async def update_board(c: Client, m: Message, up_board):
    await asyncio.sleep(3)      # just a random delay for no reason
    await c.edit_message_reply_markup(
        m.chat.id,
        m.message_id,
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{up_board[1]}", callback_data="tic1"),
                    InlineKeyboardButton(f"{up_board[2]}", callback_data="tic2"),
                    InlineKeyboardButton(f"{up_board[3]}", callback_data="tic3")
                ],
                [
                    InlineKeyboardButton(f"{up_board[4]}", callback_data="tic4"),
                    InlineKeyboardButton(f"{up_board[5]}", callback_data="tic5"),
                    InlineKeyboardButton(f"{up_board[6]}", callback_data="tic6")
                ],
                [
                    InlineKeyboardButton(f"{up_board[7]}", callback_data="tic7"),
                    InlineKeyboardButton(f"{up_board[8]}", callback_data="tic8"),
                    InlineKeyboardButton(f"{up_board[9]}", callback_data="tic9")
                ]
            ]
        )
    )

    # update the board:
    await RoanuTicTacToe().update_board(m.chat.id, m.message_id, up_board)


@Client.on_message(Filters.command(commands=['tictactoe'], prefixes=['/', '!']))
async def tictactoe_command(c: Client, m: Message):
    new_board = [' ' for x in range(10)]
    tic_message = await m.reply_text(
        text=f"{Emoji.PERSON_FENCING} Lets play {Emoji.PERSON_FENCING}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{new_board[1]}", callback_data="tic1"),
                    InlineKeyboardButton(f"{new_board[2]}", callback_data="tic2"),
                    InlineKeyboardButton(f"{new_board[3]}", callback_data="tic3")
                ],
                [
                    InlineKeyboardButton(f"{new_board[4]}", callback_data="tic4"),
                    InlineKeyboardButton(f"{new_board[5]}", callback_data="tic5"),
                    InlineKeyboardButton(f"{new_board[6]}", callback_data="tic6")
                ],
                [
                    InlineKeyboardButton(f"{new_board[7]}", callback_data="tic7"),
                    InlineKeyboardButton(f"{new_board[8]}", callback_data="tic8"),
                    InlineKeyboardButton(f"{new_board[9]}", callback_data="tic9")
                ]
            ]
        )
    )

    # insert the new board to DB:
    await RoanuTicTacToe().new_game(
        chat_id=m.chat.id,
        from_id=m.from_user.id,
        message_id=tic_message.message_id,
        board=new_board
    )


@Client.on_callback_query()
async def cb_tic_query(c: Client, cb: CallbackQuery):
    cb_pos = int(cb.data.strip("tic"))
    should_roanu_play = False

    board_document = await RoanuTicTacToe().find_board(cb.message.chat.id, cb.message.message_id)
    board = board_document["board"]
    owner = board_document["from_id"]

    if cb.from_user.id == owner:
        if not (await is_winner(board, '✔️')):
            if await is_space_free(cb_pos, board):
                await cb.answer()
                await insert_play("✖️", cb_pos, board)
                try:
                    await update_board(c, cb.message, board)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await update_board(c, cb.message, board)
                except Exception as e:
                    logging.error(e)

                if await is_winner(board, '✖️'):
                    try:
                        await c.edit_message_text(
                            cb.message.chat.id,
                            cb.message.message_id,
                            text=f"{Emoji.PARTY_POPPER} {Emoji.PARTYING_FACE} "
                                 f"{cb.from_user.last_name if cb.from_user.last_name else cb.from_user.username}"
                                 f" won this game!. {Emoji.PARTYING_FACE} {Emoji.PARTY_POPPER}"
                        )
                        await update_board(c, cb.message, board)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        await c.edit_message_text(
                            cb.message.chat.id,
                            cb.message.message_id,
                            text=f"{Emoji.PARTY_POPPER} {Emoji.PARTYING_FACE} "
                                 f"{cb.from_user.last_name if cb.from_user.last_name else cb.from_user.username}"
                                 f" won this game!. {Emoji.PARTYING_FACE} {Emoji.PARTY_POPPER}"
                        )
                        await update_board(c, cb.message, board)
                    except Exception as e:
                        logging.error(e)

                else:
                    should_roanu_play = True
            else:
                await cb.answer(f"The position is not free! {Emoji.MAN_SHRUGGING_DARK_SKIN_TONE}")

        elif await is_winner(board, '✔️'):
            should_roanu_play = False
            await cb.answer(f"Roanu won this game already! {Emoji.MAN_SHRUGGING_DARK_SKIN_TONE}", show_alert=True)

        if should_roanu_play:
            if not (await is_winner(board, '✖️')):
                move = await roanu_move(board)
                if move == 0:
                    try:
                        await c.edit_message_text(
                            cb.message.chat.id,
                            cb.message.message_id,
                            text=f"{Emoji.CONSTRUCTION} This game is a tie {Emoji.CONSTRUCTION}"
                        )
                        await update_board(c, cb.message, board)
                    except FloodWait as e:
                        await c.edit_message_text(
                            cb.message.chat.id,
                            cb.message.message_id,
                            text=f"{Emoji.CONSTRUCTION} This game is a tie {Emoji.CONSTRUCTION}"
                        )
                        await update_board(c, cb.message, board)
                    except Exception as e:
                        logging.error(e)
                else:
                    await insert_play("✔️", move, board)
                    try:
                        await update_board(c, cb.message, board)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        await update_board(c, cb.message, board)
                    except Exception as e:
                        logging.error(e)

                    if await is_winner(board, '✔️'):
                        try:
                            await c.edit_message_text(
                                cb.message.chat.id,
                                cb.message.message_id,
                                text=f"{Emoji.PARTY_POPPER} {Emoji.PARTYING_FACE} Roanu"
                                     f" won this game!. {Emoji.PARTYING_FACE} {Emoji.PARTY_POPPER}"
                            )
                            await update_board(c, cb.message, board)
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await c.edit_message_text(
                                cb.message.chat.id,
                                cb.message.message_id,
                                text=f"{Emoji.PARTY_POPPER} {Emoji.PARTYING_FACE} Roanu"
                                     f" won this game!. {Emoji.PARTYING_FACE} {Emoji.PARTY_POPPER}"
                            )
                            await update_board(c, cb.message, board)
                        except Exception as e:
                            logging.error(e)

            elif await is_winner(board, '✖️'):
                await cb.answer(f"{cb.from_user.last_name if cb.from_user.last_name else cb.from_user.username}"
                                f" won this game already!. {Emoji.MAN_SHRUGGING_DARK_SKIN_TONE}", show_alert=True)

    else:
        owner_user_object = cb.from_user
        if cb.message.chat.type == "group" or cb.message.chat.type == "supergroup":
            owner_user_object = await c.get_chat_member(cb.message.chat.id, owner)
        await cb.answer(f"This game is owned by "
                        f"{owner_user_object.user.last_name if owner_user_object.user.last_name else owner_user_object.user.username}, "
                        f"You are not allowed to do a move {Emoji.MAN_GESTURING_NO_DARK_SKIN_TONE}, "
                        f"if you wish to play a new game send the command "
                        f"/tictactoe {Emoji.MAN_SHRUGGING_DARK_SKIN_TONE}", show_alert=True)
