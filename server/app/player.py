import json
import random

from app.helpers import read_file


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.cards = None
        self.is_judge = False

        self.deal_cards()

    def to_json(self):
        return self.__dict__

    def deal_cards(self):
        # TODO: store cards in session and prevent duplicates between players
        self.cards = random.sample(read_file('responses.json'), 5)
