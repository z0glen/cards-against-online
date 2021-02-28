import unittest

from app.player import Player
from app.game import Game


class TestPlayer(unittest.TestCase):
    def test_deal_cards(self):
        p = Player("test", Game(), "testsid")
        self.assertEqual(len(p.cards), 7)
        p.deal_cards()
        self.assertEqual(len(p.cards), 14)

    def test_play_card(self):
        g = Game()
        p = Player("test", g, "testsid")
        g.draw_black_card()
        p.play_card(p.cards[0]["id"])
        self.assertEqual(len(p.cards), 6)

    def test_play_invalid_card(self):
        g = Game()
        p = Player("test", g, "testsid")
        g.draw_black_card()
        self.assertRaises(TypeError, p.play_card, "invalid")
        self.assertEqual(len(p.cards), 7)


if __name__ == '__main__':
    unittest.main()
