import random
import string

class Game:
    def __init__(self):
        self.id = self.generate_game_code()
        self.players = set()

    @staticmethod
    def generate_game_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
