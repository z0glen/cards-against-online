import random
import string
import json

from app.helpers import read_file


class Game:
    def __init__(self):
        self.id = self.generate_game_code()
        self.state = 'lobby'
        self.black_card = None
        self.players = {}
        self.judge = None

    @staticmethod
    def generate_game_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

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
            if not p.playedCard:
                return False
        return True
