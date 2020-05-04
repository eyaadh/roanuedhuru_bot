from roanu.utils.database import RoanuDB


class RoanuScores:
    def __init__(self):
        self.collection_crossword = RoanuDB().db['scores']
