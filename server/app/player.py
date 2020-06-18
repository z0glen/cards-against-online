import json
import random

from app.helpers import read_file


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.cards = None
        self.is_judge = False
        self.playedCard = None

        self.deal_cards()

    def to_json(self):
        return self.__dict__

    def deal_cards(self):
        # TODO: store cards in session and prevent duplicates between players
        self.cards = random.sample(read_file('responses.json'), 5)

    def card_index_from_id(self, card_id):
        for idx, card in enumerate(self.cards):
            if card["id"] == card_id:
                return idx

    def play_card(self, card_id):
        card_idx = self.card_index_from_id(card_id)
        print(card_id)
        print(card_idx)
        self.playedCard = self.cards.pop(card_idx)
        print(self.playedCard)
