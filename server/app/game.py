import random
import string
import json

from app.helpers import read_file


class Game:
    def __init__(self):
        self.id = self.generate_game_code()
        self.deck = {}
        self.state = 'lobby'
        self.black_card = None
        self.players = {}
        self.judge = None
        self.played_cards = {}

        self.load_cards()

    @staticmethod
    def generate_game_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def load_cards(self):
        self.deck['calls'] = read_file('calls.json')
        self.deck['responses'] = read_file('responses.json')

    def to_json(self):
        ps = {}
        for name, player in self.players.items():
            ps[name] = player.to_json()
        obj = {
            "id": self.id,
            "state": self.state,
            "black_card": self.black_card,
            "players": ps
        }
        return json.dumps(obj)

    def draw_black_card(self):
        # TODO: prevent duplicates between rounds
        self.black_card = random.sample(read_file('calls.json'), 1)

    def assign_judge(self):
        self.judge = random.sample(self.players.keys(), 1)[0]
        print(self.judge)
        self.reset_judging()
        self.players[self.judge].is_judge = True

    def reset_judging(self):
        for name, p in self.players.items():
            p.is_judge = False

    def find_player_by_name(self, name):
        for n, p in self.players.items():
            if n == name:
                return p

    def has_all_played(self):
        for n, p in self.players.items():
            if not p.playedCard and not p.is_judge:
                return False
        return True

    def find_card_by_id(self, card_id):
        for card in self.deck['responses']:
            if card.id == card_id:
                return card

    def award_point(self, card_id):
        print(self.played_cards)
        for name, card in self.played_cards.items():
            print(card)
            if card['id'] == card_id:
                self.find_player_by_name(name).score += 1
                self.end_round()

    def end_round(self):
        self.played_cards = {}
        for name, p in self.players.items():
            p.is_judge = False
            p.playedCard = None
            p.handle_cards()
        self.assign_judge()
        self.draw_black_card()
