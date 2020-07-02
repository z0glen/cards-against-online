import random

class Player:
    def __init__(self, name, game):
        self.game = game

        self.name = name
        self.score = 0
        self.cards = None
        self.is_judge = False
        self.playedCard = []
        self.can_play_card = True
        self.judge_num = 0

        self.deal_cards()

    def to_json(self):
        return {
            'name': self.name,
            'score': self.score,
            'cards': self.cards,
            'is_judge': self.is_judge,
            'playedCard': self.playedCard,
            'canPlayCard': self.can_play_card,
        }

    def deal_cards(self):
        # TODO: prevent duplicates between players
        self.cards = random.sample(self.game.deck['responses'], 5)

    def card_index_from_id(self, card_id):
        print("card_index_from_id")
        for idx, card in enumerate(self.cards):
            if card["id"] == card_id:
                return idx

    def play_card(self, card_id):
        card_idx = self.card_index_from_id(card_id)
        played_card = self.cards.pop(card_idx)
        self.playedCard.append(played_card)
        print(self.playedCard)
        print(len(self.playedCard))
        print(len(self.game.black_card['text']))
        if len(self.playedCard) == len(self.game.black_card['text']) - 1:
            self.can_play_card = False
        return played_card

    def handle_cards(self):
        if len(self.cards) < 5:
            num_cards = 5 - len(self.cards)
            self.cards.extend(random.sample(self.game.deck['responses'], num_cards))
