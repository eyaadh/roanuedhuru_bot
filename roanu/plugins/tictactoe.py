from pyrogram import Client, Message, Filters, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

board = [' ' for x in range(10)]
tic_message = None


async def insert_play(letter, pos):
    board[pos] = letter


async def is_space_free(pos):
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


async def roanu_move():
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
    await c.edit_message_reply_markup(
        m.chat.id,
        m.message_id,
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{board[1]}", callback_data="tic1"),
                    InlineKeyboardButton(f"{board[2]}", callback_data="tic2"),
                    InlineKeyboardButton(f"{board[3]}", callback_data="tic3")
                ],
                [
                    InlineKeyboardButton(f"{board[4]}", callback_data="tic4"),
                    InlineKeyboardButton(f"{board[5]}", callback_data="tic5"),
                    InlineKeyboardButton(f"{board[6]}", callback_data="tic6")
                ],
                [
                    InlineKeyboardButton(f"{board[7]}", callback_data="tic7"),
                    InlineKeyboardButton(f"{board[8]}", callback_data="tic8"),
                    InlineKeyboardButton(f"{board[9]}", callback_data="tic9")
                ]
            ]
        )
    )


@Client.on_message(Filters.command(commands=['tictactoe'], prefixes=['/', '!']))
async def tictactoe_command(c: Client, m: Message):
    global tic_message

    tic_message = await m.reply_text(
        text="Yo lets play",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{board[1]}", callback_data="tic1"),
                    InlineKeyboardButton(f"{board[2]}", callback_data="tic2"),
                    InlineKeyboardButton(f"{board[3]}", callback_data="tic3")
                ],
                [
                    InlineKeyboardButton(f"{board[4]}", callback_data="tic4"),
                    InlineKeyboardButton(f"{board[5]}", callback_data="tic5"),
                    InlineKeyboardButton(f"{board[6]}", callback_data="tic6")
                ],
                [
                    InlineKeyboardButton(f"{board[7]}", callback_data="tic7"),
                    InlineKeyboardButton(f"{board[8]}", callback_data="tic8"),
                    InlineKeyboardButton(f"{board[9]}", callback_data="tic9")
                ]
            ]
        )
    )


@Client.on_callback_query()
async def cb_tic_query(c: Client, cb: CallbackQuery):
    cb_pos = int(cb.data.strip("tic"))
    comp_play = False
    if not (await is_winner(board, '✔️')):
        if await is_space_free(cb_pos):
            await cb.answer()
            await insert_play("✖️", cb_pos)
            await update_board(c, cb.message, board)

            if await is_winner(board, '✖️'):
                await cb.answer(f"{cb.from_user.last_name if cb.from_user.last_name else cb.from_user.username}"
                                f" won the game!.")
            else:
                comp_play = True
        else:
            await cb.answer("The position is not free!")
    elif await is_winner(board, '✔️'):
        comp_play = False
        await cb.answer("Roanu won this game already!")

    if comp_play:
        if not (await is_winner(board, '✖️')):
            move = await roanu_move()
            if move == 0:
                await cb.answer("The game is a tie!")
            else:
                await insert_play("✔️", move)
                await update_board(c, cb.message, board)

                if await is_winner(board, '✔️'):
                    await cb.answer("Roanu won this game!")

        elif await is_winner(board, '✖️'):
            await cb.answer(f"{cb.from_user.last_name if cb.from_user.last_name else cb.from_user.username}"
                            f" won this game already!.")
