import unittest
from unittest.mock import Mock, patch

import numpy as np
from src.utils.deck import Card, Suit
from src.utils.hand import Hand, HandChecker


class TestHand(unittest.TestCase):
    def test_add_card(self):
        hand = Hand()
        card = Card(4, Suit.club.name)
        hand.add_card(card)
        self.assertListEqual(hand.cards, [card])

    def test_get_hand_matrix(self):
        hand = Hand()
        hand.cards = [Card(2, Suit.heart.name), Card(2, Suit.club.name)]
        card_sum = hand.get_hand_matrix()
        expected = np.zeros((4, 13))
        expected[Suit.heart.value, 0] = 1
        expected[Suit.club.value, 0] = 1
        self.assertTrue(np.array_equal(card_sum, expected))


class TestHandCheck(unittest.TestCase):
    def setUp(self):
        self.hand_checker = HandChecker()
        self.high_card_queen = [
            Card(2, Suit.diamond.name),
            Card(3, Suit.club.name),
            Card(7, Suit.heart.name),
            Card(10, Suit.spade.name),
            Card(11, Suit.heart.name),
            Card(12, Suit.heart.name),
            Card(9, Suit.heart.name),
        ]
        self.pair_twos = [
            Card(2, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.diamond.name),
            Card(11, Suit.club.name),
            Card(2, Suit.diamond.name),
            Card(8, Suit.diamond.name),
            Card(7, Suit.diamond.name),
        ]
        self.two_pair_4_8 = [
            Card(4, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(8, Suit.club.name),
            Card(4, Suit.heart.name),
            Card(8, Suit.diamond.name),
            Card(7, Suit.diamond.name),
        ]
        self.three_of_a_kind_4 = [
            Card(4, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(8, Suit.club.name),
            Card(4, Suit.heart.name),
            Card(4, Suit.diamond.name),
            Card(7, Suit.diamond.name),
        ]
        self.straight_11_high = [
            Card(5, Suit.club.name),
            Card(6, Suit.diamond.name),
            Card(7, Suit.spade.name),
            Card(8, Suit.heart.name),
            Card(9, Suit.heart.name),
            Card(10, Suit.heart.name),
            Card(11, Suit.heart.name),
        ]
        self.straight_10_high = [
            Card(5, Suit.club.name),
            Card(6, Suit.diamond.name),
            Card(7, Suit.spade.name),
            Card(8, Suit.heart.name),
            Card(9, Suit.heart.name),
            Card(10, Suit.heart.name),
            Card(14, Suit.heart.name),
        ]
        self.flush_ace_high = [
            Card(14, Suit.heart.name),
            Card(13, Suit.heart.name),
            Card(2, Suit.heart.name),
            Card(7, Suit.heart.name),
            Card(5, Suit.heart.name),
            Card(8, Suit.spade.name),
            Card(2, Suit.spade.name),
        ]
        self.four_of_a_kind_3 = [
            Card(3, Suit.spade.name),
            Card(3, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(8, Suit.club.name),
            Card(3, Suit.heart.name),
            Card(3, Suit.diamond.name),
            Card(7, Suit.diamond.name),
        ]
        self.straight_flush_8_high = [
            Card(4, Suit.heart.name),
            Card(5, Suit.heart.name),
            Card(6, Suit.heart.name),
            Card(7, Suit.heart.name),
            Card(8, Suit.heart.name),
            Card(3, Suit.heart.name),
            Card(10, Suit.heart.name),
        ]
        self.wheel_fush = [
            Card(4, Suit.heart.name),
            Card(5, Suit.heart.name),
            Card(3, Suit.heart.name),
            Card(2, Suit.heart.name),
            Card(14, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(10, Suit.heart.name),
        ]

    def test_get_value_array(self):
        hand = Hand()
        hand.add_card(Card(3, Suit.club.name))
        hand.add_card(Card(3, Suit.diamond.name))
        hand.add_card(Card(10, Suit.diamond.name))
        hand_matrix = hand.get_hand_matrix()
        expected = np.zeros(13)
        expected[1] = 2
        expected[8] = 1
        actual = self.hand_checker.get_value_array(hand_matrix)
        self.assertTrue(np.array_equal(expected, actual))

    def test_check_connected(self):
        test_array = np.zeros(13)
        for i in range(5):
            test_array[i + 3] = 2
        connect = self.hand_checker.check_connected(test_array)
        self.assertEqual(connect, 7)

        wheel_array = np.zeros(13)
        for i in range(4):
            wheel_array[i] = 1
        wheel_array[12] = 1
        connect = self.hand_checker.check_connected(wheel_array)
        self.assertEqual(connect, 3)

    def get_hand(self, cards):
        hand = Hand()
        for c in cards:
            hand.add_card(c)
        return hand

    def test_get_suit_array(self):
        hand = self.get_hand(
            [
                Card(2, Suit.club.name),
                Card(3, Suit.club.name),
                Card(12, Suit.diamond.name),
            ]
        )
        suit_array = self.hand_checker.get_suit_array(hand.get_hand_matrix())
        expected = np.zeros((4,))
        expected[Suit.club.value] = 2
        expected[Suit.diamond.value] = 1
        self.assertTrue(np.array_equal(suit_array, expected))

    def test_check_high_card(self):
        hand = self.get_hand(
            [
                Card(2, Suit.club.name),
                Card(3, Suit.club.name),
                Card(14, Suit.diamond.name),
            ]
        )
        high_card = self.hand_checker.check_high_card(hand)
        self.assertDictEqual(high_card, {"hand_type": "high_card", "value": 14})

    def test_check_pair(self):
        cards = self.pair_twos
        hand = self.get_hand(cards)
        pair_info = self.hand_checker.check_pair(hand)
        self.assertDictEqual(
            pair_info,
            {"value": 2, "hand_type": "pair"},
            "error where pairs exist",
        )

        cards = [
            Card(2, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.diamond.name),
            Card(11, Suit.club.name),
            Card(5, Suit.diamond.name),
            Card(8, Suit.diamond.name),
            Card(7, Suit.diamond.name),
        ]
        hand = self.get_hand(cards)
        pair_info = self.hand_checker.check_pair(hand)
        self.assertFalse(pair_info, "error with no pairs")
        self.assertFalse(
            self.hand_checker.check_pair(self.get_hand(self.high_card_queen))
        )

    def test_check_two_pair(self):
        # High card
        self.assertFalse(
            self.hand_checker.check_two_pair(
                self.get_hand(self.high_card_queen),
            ),
            "error when checking against high card",
        )
        # pair of 2s
        self.assertFalse(
            self.hand_checker.check_two_pair(self.get_hand(self.pair_twos)),
            "error when checking against pair",
        )
        hand = self.get_hand(self.two_pair_4_8)
        two_pair_info = self.hand_checker.check_two_pair(hand)
        self.assertDictEqual(
            two_pair_info, {"value": (4, 8), "hand_type": "two_pair"}
        )

    def test_three_of_a_kind(self):
        # high card
        self.assertFalse(
            self.hand_checker.check_three_of_a_kind(
                self.get_hand(self.high_card_queen)
            )
        )
        self.assertIsNotNone(
            self.hand_checker.check_three_of_a_kind(
                self.get_hand(self.high_card_queen)
            )
        )
        hand = self.get_hand(self.three_of_a_kind_4)
        expected = {"value": 4, "hand_type": "three_of_a_kind"}
        self.assertDictEqual(
            expected, self.hand_checker.check_three_of_a_kind(hand)
        )

    def test_check_straight(self):
        hand = self.get_hand(self.high_card_queen)
        self.assertFalse(self.hand_checker.check_straight(hand))
        hand = self.get_hand(self.two_pair_4_8)
        self.assertFalse(self.hand_checker.check_straight(hand))
        hand = self.get_hand(self.three_of_a_kind_4)
        self.assertFalse(self.hand_checker.check_straight(hand))

        hand = self.get_hand(self.straight_11_high)
        expected = {"value": 11, "hand_type": "straight"}
        self.assertDictEqual(expected, self.hand_checker.check_straight(hand))

        hand = self.get_hand(self.straight_10_high)
        expected = {"value": 10, "hand_type": "straight"}
        self.assertDictEqual(expected, self.hand_checker.check_straight(hand))

    def test_check_flush(self):
        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, "pair"),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, "straight"),
            (self.three_of_a_kind_4, "three of a kind"),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_flush(hand),
                f"error with {name} in check flush",
            )
        hand = self.get_hand(self.flush_ace_high)
        expected = {"value": 14, "hand_type": "flush"}
        flush_info = self.hand_checker.check_flush(hand)
        self.assertDictEqual(flush_info, expected)

    def test_check_four_of_a_kind(self):
        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, "pair"),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, "straight"),
            (self.three_of_a_kind_4, "three of a kind"),
            (self.flush_ace_high, "flush"),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_four_of_a_kind(hand),
                f"error with {name} in check four of a kind",
            )
        hand = self.get_hand(self.four_of_a_kind_3)
        hand_info = self.hand_checker.check_four_of_a_kind(hand)
        expected = {"hand_type": "four_of_a_kind", "value": 3}
        self.assertDictEqual(expected, hand_info)

    def test_check_straight_flush(self):

        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, "pair"),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, "straight"),
            (self.three_of_a_kind_4, "three of a kind"),
            (self.flush_ace_high, "flush"),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_straight_flush(hand),
                f"error with {name} in check straight flush",
            )

        hand = self.get_hand(self.straight_flush_8_high)
        expected = {"hand_type": "straight_flush", "value": 8}
        actual = self.hand_checker.check_straight_flush(hand)
        self.assertDictEqual(expected, actual)

        hand = self.get_hand(self.wheel_fush)
        expected = {"hand_type": "straight_flush", "value": 5}
        actual = self.hand_checker.check_straight_flush(hand)
        self.assertDictEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
