from roanu.utils.database import RoanuDB


class RoanuCrossword:
    def __init__(self):
        self.collection_crossword = RoanuDB().db['crossword']

    async def insert_messages(self, chat_id, message_id, word, shuffled):
        query = {"chat_id": chat_id, "message_id": message_id}
        if self.collection_crossword.count(query) == 0:
            self.collection_crossword.insert_one(
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "word": word,
                    "shuffled": shuffled
                }
            )

    async def find_message(self, chat_id, message_id):
        query = {"chat_id": chat_id, "message_id": message_id}
        if self.collection_crossword.count(query) > 0:
            return self.collection_crossword.find_one(query)
        else:
            return False

    async def update_answer(self, chat_id, message_id):
        query = {"chat_id": chat_id, "message_id": message_id}
        if self.collection_crossword.count(query) > 0:
            return self.collection_crossword.update_one(query, {"$set": {"answered": True}})
