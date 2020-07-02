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
        self.judge_num = 0

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
        self.black_card = random.sample(self.deck['calls'], 1)[0]

    def assign_judge(self):
        for name, p in self.players.items():
            if p.judge_num == self.judge_num:
                self.judge = name
        # self.judge = random.sample(self.players.keys(), 1)[0]
        print(self.judge)
        self.reset_judging()
        self.players[self.judge].is_judge = True
        self.players[self.judge].can_play_card = False

    def reset_judging(self):
        for name, p in self.players.items():
            p.is_judge = False

    def find_player_by_name(self, name):
        for n, p in self.players.items():
            if n == name:
                return p

    def has_all_played(self):
        for n, p in self.players.items():
            print(p.to_json())
            if p.can_play_card:
                print("Player " + p.name + " has not finished playing")
                return False
        return True

    def find_card_by_id(self, card_id):
        for card in self.deck['responses']:
            if card.id == card_id:
                return card

    def award_point(self, card_id):
        print(self.played_cards)
        for name, cards in self.played_cards.items():
            print(cards)
            for card in cards:
                print(card)
                if card['id'] == card_id:
                    self.find_player_by_name(name).score += 1
                    self.end_round()

    def end_round(self):
        self.played_cards = {}
        for name, p in self.players.items():
            p.is_judge = False
            p.playedCard = []
            p.can_play_card = True
            p.handle_cards()
        if self.judge_num >= len(self.players) - 1:
            self.judge_num = 0
        else:
            self.judge_num += 1
        self.assign_judge()
        self.draw_black_card()

    def add_player(self, player):
        self.players[player.name] = player
        player.judge_num = len(self.players) - 1
