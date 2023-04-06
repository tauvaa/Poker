import unittest
from unittest.mock import Mock, patch

import numpy as np
from src.utils.deck import Card, Suit
from src.utils.hand import Hand, HandChecker, HandOrder


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


class TestHandChecker(unittest.TestCase):
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
        self.high_card_king = [
            Card(2, Suit.diamond.name),
            Card(3, Suit.club.name),
            Card(7, Suit.heart.name),
            Card(10, Suit.spade.name),
            Card(11, Suit.heart.name),
            Card(13, Suit.heart.name),
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
        self.two_pair_4_8_10 = [
            Card(4, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(8, Suit.club.name),
            Card(4, Suit.heart.name),
            Card(8, Suit.diamond.name),
            Card(10, Suit.diamond.name),
        ]
        self.two_pair_4_5 = [
            Card(4, Suit.club.name),
            Card(3, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(5, Suit.club.name),
            Card(4, Suit.heart.name),
            Card(5, Suit.diamond.name),
            Card(10, Suit.diamond.name),
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
        self.full_house_6_9 = [
            Card(6, Suit.heart.name),
            Card(6, Suit.club.name),
            Card(6, Suit.spade.name),
            Card(9, Suit.diamond.name),
            Card(9, Suit.club.name),
            Card(12, Suit.spade.name),
            Card(11, Suit.club.name),
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

    def test_get_kicker(self):
        card_array = np.zeros(13)
        card_array = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        card_array = np.array(card_array)
        kicker = self.hand_checker.get_kicker(card_array, 1)
        self.assertListEqual(kicker, [14])

        card_array = np.zeros(13)
        card_array = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        card_array = np.array(card_array)
        kicker = self.hand_checker.get_kicker(card_array, 2)
        self.assertListEqual(kicker, [14, 10])

    def test_get_max_greater_index(self):
        array = np.zeros(13)
        array[9] = 1
        array[5] = 3
        max_value = self.hand_checker.get_max_greater_index(array, 1)
        self.assertEqual(max_value, 5)

        array = np.zeros(13)
        array[9] = 1
        array[5] = 3
        array[7] = 2

        max_value = self.hand_checker.get_max_greater_index(array, 1)
        self.assertEqual(max_value, 7)

        max_value = self.hand_checker.get_max_greater_index(array, 2)
        self.assertEqual(max_value, 5)

        max_value = self.hand_checker.get_max_greater_index(array, 10)
        self.assertIsNone(max_value)

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
                Card(4, Suit.club.name),
                Card(8, Suit.club.name),
                Card(9, Suit.club.name),
                Card(14, Suit.diamond.name),
            ]
        )
        high_card = self.hand_checker.check_high_card(hand)
        self.assertDictEqual(
            high_card,
            {
                "hand_type": HandOrder.high_card.name,
                "value": 14,
                "kickers": [9, 8, 4, 3],
            },
        )

    def test_check_pair(self):
        cards = self.pair_twos
        hand = self.get_hand(cards)
        pair_info = self.hand_checker.check_pair(hand)
        self.assertDictEqual(
            pair_info,
            {
                "value": 2,
                "hand_type": HandOrder.pair.name,
                "kickers": [11, 10, 8],
            },
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
            two_pair_info,
            {"value": (8, 4), "hand_type": HandOrder.two_pair.name},
        )

        # check when you have 3 pairs you take top 2
        hand = self.get_hand(self.two_pair_4_8_10)
        actual = self.hand_checker.check_two_pair(hand)
        expected = {"hand_type": HandOrder.two_pair.name, "value": (10, 8)}
        self.assertDictEqual(actual, expected)

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
        expected = {
            "value": 4,
            "hand_type": HandOrder.three_of_a_kind.name,
            "kickers": [10, 8],
        }
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
        expected = {"value": 11, "hand_type": HandOrder.straight.name}
        self.assertDictEqual(expected, self.hand_checker.check_straight(hand))

        hand = self.get_hand(self.straight_10_high)
        expected = {"value": 10, "hand_type": HandOrder.straight.name}
        self.assertDictEqual(expected, self.hand_checker.check_straight(hand))

    def test_check_flush(self):
        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, HandOrder.pair.name),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, HandOrder.straight.name),
            (self.three_of_a_kind_4, "three of a kind"),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_flush(hand),
                f"error with {name} in check flush",
            )
        hand = self.get_hand(self.flush_ace_high)
        expected = {"value": 14, "hand_type": HandOrder.flush.name}
        flush_info = self.hand_checker.check_flush(hand)
        self.assertDictEqual(flush_info, expected)

    def test_check_four_of_a_kind(self):
        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, HandOrder.pair.name),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, HandOrder.straight.name),
            (self.three_of_a_kind_4, "three of a kind"),
            (self.flush_ace_high, HandOrder.flush.name),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_four_of_a_kind(hand),
                f"error with {name} in check four of a kind",
            )
        hand = self.get_hand(self.four_of_a_kind_3)
        hand_info = self.hand_checker.check_four_of_a_kind(hand)
        expected = {
            "hand_type": HandOrder.four_of_a_kind.name,
            "value": 3,
            "kickers": [10],
        }
        self.assertDictEqual(expected, hand_info)

    def test_check_full_house(self):
        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, HandOrder.pair.name),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, HandOrder.straight.name),
            (self.three_of_a_kind_4, "three of a kind"),
            (self.flush_ace_high, HandOrder.flush.name),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_full_house(hand),
                f"erro with {name} in check full house",
            )

        expected = {"hand_type": "full_house", "value": (6, 9)}
        hand = self.get_hand(self.full_house_6_9)
        actual = self.hand_checker.check_full_house(hand)
        self.assertDictEqual(expected, actual)

    def test_check_straight_flush(self):

        for cards, name in [
            (self.high_card_queen, "high card"),
            (self.pair_twos, HandOrder.pair.name),
            (self.two_pair_4_8, "2 pair"),
            (self.straight_10_high, HandOrder.straight.name),
            (self.three_of_a_kind_4, "three of a kind"),
            (self.flush_ace_high, HandOrder.flush.name),
        ]:
            hand = self.get_hand(cards)
            self.assertFalse(
                self.hand_checker.check_straight_flush(hand),
                f"error with {name} in check straight flush",
            )

        hand = self.get_hand(self.straight_flush_8_high)
        expected = {"hand_type": HandOrder.straight_flush.name, "value": 8}
        actual = self.hand_checker.check_straight_flush(hand)
        self.assertDictEqual(expected, actual)

        hand = self.get_hand(self.wheel_fush)
        expected = {"hand_type": HandOrder.straight_flush.name, "value": 5}
        actual = self.hand_checker.check_straight_flush(hand)
        self.assertDictEqual(expected, actual)

    def test_get_hand(self):
        hand = self.get_hand(self.high_card_queen)
        actual = self.hand_checker.get_hand(hand)
        expected = {
            "hand_type": HandOrder.high_card.name,
            "value": 12,
            "kickers": [11, 10, 9, 7],
        }
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.pair_twos)
        actual = self.hand_checker.get_hand(hand)
        expected = {
            "hand_type": HandOrder.pair.name,
            "value": 2,
            "kickers": [11, 10, 8],
        }
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.two_pair_4_8)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.two_pair.name, "value": (8, 4)}
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.three_of_a_kind_4)
        actual = self.hand_checker.get_hand(hand)
        expected = {
            "hand_type": HandOrder.three_of_a_kind.name,
            "value": 4,
            "kickers": [10, 8],
        }
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.straight_11_high)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.straight.name, "value": 11}
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.flush_ace_high)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.flush.name, "value": 14}
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.full_house_6_9)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.full_house.name, "value": (6, 9)}
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.four_of_a_kind_3)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.four_of_a_kind.name, "value": 3, "kickers": [10]}
        self.assertDictEqual(actual, expected)

        hand = self.get_hand(self.straight_flush_8_high)
        actual = self.hand_checker.get_hand(hand)
        expected = {"hand_type": HandOrder.straight_flush.name, "value": 8}
        self.assertDictEqual(actual, expected)

    def test_compare_hands(self):
        hand1 = self.get_hand(self.high_card_queen)
        hand2 = self.get_hand(self.pair_twos)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand2")

        hand1 = self.get_hand(self.full_house_6_9)
        hand2 = self.get_hand(self.pair_twos)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand1")

    def test_compare_hand_same_hand_type(self):
        hand1 = self.get_hand(self.high_card_queen)
        hand2 = self.get_hand(self.high_card_king)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand2")

        hand1 = self.get_hand(self.two_pair_4_8)
        hand2 = self.get_hand(self.two_pair_4_8_10)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand2")

        hand1 = self.get_hand(self.two_pair_4_8)
        hand2 = self.get_hand(self.two_pair_4_5)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand2")

        hand1 = self.get_hand(self.straight_10_high)
        hand2 = self.get_hand(self.straight_11_high)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand2")

    def test_compare_hand_kickers(self):
        hand1 = [
            Card(2, Suit.heart.name),
            Card(3, Suit.diamond.name),
            Card(7, Suit.club.name),
            Card(9, Suit.spade.name),
            Card(10, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(5, Suit.spade.name),
        ]
        hand1 = self.get_hand(hand1)

        hand2 = [
            Card(2, Suit.heart.name),
            Card(3, Suit.diamond.name),
            Card(7, Suit.club.name),
            Card(9, Suit.spade.name),
            Card(8, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(5, Suit.spade.name),
        ]
        hand2 = self.get_hand(hand2)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand1")

        # pairs
        hand1 = [
            Card(2, Suit.heart.name),
            Card(3, Suit.diamond.name),
            Card(7, Suit.club.name),
            Card(9, Suit.spade.name),
            Card(11, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(10, Suit.spade.name),
        ]
        hand1 = self.get_hand(hand1)

        hand2 = [
            Card(2, Suit.heart.name),
            Card(3, Suit.diamond.name),
            Card(7, Suit.club.name),
            Card(9, Suit.spade.name),
            Card(11, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(5, Suit.spade.name),
        ]
        hand2 = self.get_hand(hand2)
        hand_winner = self.hand_checker.compare_hands(hand1, hand2)
        self.assertEqual(hand_winner, "hand1")


if __name__ == "__main__":
    unittest.main()
