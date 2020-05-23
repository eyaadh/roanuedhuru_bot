from roanu.utils.database import RoanuDB


class RoanuTicTacToe:
    def __init__(self):
        self.collection_ticktactoe = RoanuDB().db['tictactoe']

    async def new_game(self, chat_id, from_id, message_id, board):
        query = {"chat_id": chat_id, "message_id": message_id, "from_id": from_id}
        if self.collection_ticktactoe.count(query) == 0:
            self.collection_ticktactoe.insert_one(
                {
                    "chat_id": chat_id,
                    "from_id": from_id,
                    "message_id": message_id,
                    "board": board
                }
            )

    async def find_board(self, chat_id, message_id):
        query = {"chat_id": chat_id, "message_id": message_id}
        if self.collection_ticktactoe.count(query) > 0:
            return self.collection_ticktactoe.find_one(query)
        else:
            return False

    async def update_board(self, chat_id, message_id, board):
        query = {"chat_id": chat_id, "message_id": message_id}
        if self.collection_ticktactoe.count(query) > 0:
            self.collection_ticktactoe.update_one(query, {"$set": {"board": board}})
