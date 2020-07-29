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
        self.round_num = 1
        self.history = {}  # an int to string dict

        self.load_cards()

    @staticmethod
    def generate_game_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def load_cards(self):
        # TODO: use struct with more efficient front of list pops
        self.deck['calls'] = read_file('calls.json')
        random.shuffle(self.deck['calls'])
        self.deck['responses'] = read_file('responses.json')
        random.shuffle(self.deck['responses'])

    def to_json(self):
        ps = {}
        for name, player in self.players.items():
            ps[name] = player.to_json()
        obj = {
            "id": self.id,
            "state": self.state,
            "black_card": self.black_card,
            "players": ps,
            "history": self.history
        }
        return json.dumps(obj)

    def draw_black_card(self):
        self.black_card = self.deck['calls'].pop(0)
        self.deck['calls'].append(self.black_card)

    def assign_judge(self):
        for name, p in self.players.items():
            if p.judge_num == self.judge_num:
                self.judge = name
        self.reset_judging()
        if not self.judge:
            self.judge = self.players.keys()[0]
        self.players[self.judge].is_judge = True
        self.players[self.judge].can_play_card = False

    def reset_judging(self):
        for name, p in self.players.items():
            p.is_judge = False

    def find_player_by_name(self, name):
        for n, p in self.players.items():
            if n == name:
                return p
        return None

    def has_all_played(self):
        for n, p in self.players.items():
            if p.can_play_card:
                print("Player " + p.name + " has not finished playing")
                return False
        return True

    def find_card_by_id(self, card_id):
        for card in self.deck['responses']:
            if card.id == card_id:
                return card

    def award_point(self, card_id):
        for name, cards in self.played_cards.items():
            for card in cards:
                if card['id'] == card_id:
                    p = self.find_player_by_name(name)
                    if p:
                        p.score += 1
                    self.history[self.round_num] = name + " has won with the card '" + card['text'][0] + "'"
                    return {'player': name, 'card': card}

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
        self.round_num += 1
        self.assign_judge()
        self.draw_black_card()

    def add_player(self, player):
        self.players[player.name] = player
        player.judge_num = len(self.players) - 1

    def remove_player(self, sid):
        target = None
        for p in self.players.values():
            if p.sid == sid:
                target = p.name
        del self.players[target]

    def is_valid_username(self, name):
        for n in self.players.keys():
            if n == name:
                return False
        return True
