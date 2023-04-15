import unittest
from unittest.mock import Mock, patch

from src.utils.deck import Deck


class TestDeck(unittest.TestCase):
    def test_init(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    @patch("src.utils.deck.random.shuffle")
    def test_shuffle(self, mock_shuffle):
        deck = Deck()
        deck.shuffle()
        self.assertEqual(mock_shuffle.call_count, 1)

    def test_reset(self):
        deck = Deck()
        num_cards = len(deck.cards)
        for _ in range(10):
            deck.deal_card()
        self.assertEqual(len(deck.cards), num_cards - 10)
        deck.reset()
        self.assertEqual(len(deck.cards), num_cards)


if __name__ == "__main__":
    unittest.main()
