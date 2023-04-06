import unittest
from unittest.mock import Mock, patch

from src.player import Player
from src.utils.deck import Card, Suit


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test Player", 1000)

    @patch("src.player.Hand.add_card")
    def test_add_card(self, mock_hand):
        card = Mock()
        self.player.add_card(card)
        mock_hand.assert_called_with(card)

    def test_add_bank(self):
        self.player.update_bank(100)
        self.assertEqual(self.player.bank, 1100)

    def test_subtract_bank(self):
        self.player.update_bank(-100)
        self.assertEqual(self.player.bank, 900)

    def test_equal(self):
        player = Player("Some Player", 1000, "test_player")
        self.assertEqual(player, self.player)
        player = Player("Test Player", 1000, "not_test_player")
        self.assertNotEqual(player, self.player)


if __name__ == "__main__":
    unittest.main()
