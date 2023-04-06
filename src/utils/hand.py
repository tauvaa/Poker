"""
Functions and classes here are used for storing and checking hand data.
"""

from enum import Enum, auto

import numpy as np


class HandOrder(Enum):
    high_card = auto()
    pair = auto()
    two_pair = auto()
    three_of_a_kind = auto()
    straight = auto()
    flush = auto()
    full_house = auto()
    four_of_a_kind = auto()
    straight_flush = auto()


class Hand:
    """
    Used to represent a players hand.
    """

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Use to add card to hand."""
        self.cards.append(card)

    def get_hand_matrix(self):
        """
        Use to get hand matrix. Hand matrix is matrix representation of a hand.
        """
        return sum([x.get_card_matrix() for x in self.cards])


class HandChecker:
    """
    Used to check hand, series of methods used check possible hands.  Hands can
    have multiple true values, ie. 3 of a kind is also a pair.  Need to find
    the best hand.
    """

    def get_kicker(self, array, num_cards):
        """
        Use to get kicker for array.

        Params:
            array: np array
            num_cards: number of cards to return in kicker
        """
        kickers = np.argwhere(array > 0)

        kickers = [x[0] for x in kickers]
        kickers.sort(reverse=True)
        kickers = kickers[0:num_cards]
        kickers = [x + 2 for x in kickers]
        return kickers

    def get_max_greater_index(self, array, min_value):
        """
        Use to get the indexex of an array where the value is greater than
        min_value.  Used for getting pairs, trips, and quads.

        Params:
            array: numpy array you want to check
            min_value: minimun value you want to be greater than
        """
        to_ret = -1
        for i in range(len(array)):
            if array[i] > min_value:
                to_ret = i
        if to_ret > -1:
            return to_ret
        return None

    def check_connected(self, array):
        """
        Use to check the connected squences in an array.  Used in checking
        for straigts. Returns the index of the highest 5 or more connected
        value, not the value itself.  (Returning 4 would indicate the highest
        connected value is 6)
        """

        straight_counter = 0  # used to tell how many in a row you have
        straight_found = False  # used to tell if you found a straight or not
        high_value = 0
        for i in range(len(array)):
            if array[i] > 0:
                straight_counter += 1
                if straight_counter >= 5:
                    high_value = i
                    straight_found = True
            else:

                straight_counter = 0  # reset straight counter
        if straight_found:
            return high_value
        # wheel check
        wheel_indexes = list(range(4)) + [12]
        if all([array[i] > 0 for i in wheel_indexes]):
            return 3
        return False

    def get_value_array(self, hand_matrix):
        """
        Use to transform hand matrix in value array (an array which
        contains only value information, no suit information)
        """
        return np.matmul(np.ones(4), hand_matrix)

    def get_suit_array(self, hand_matrix):
        """
        Use to transform hand matrix to suit array (an array which contains
        only suit information, no value info)
        """
        return np.matmul(hand_matrix, np.ones(13))

    def check_high_card(self, hand):
        """
        Use to get hand high card.

        Params:
            hand: Hand object
        """
        value = max([x.value for x in hand.cards])
        kickers = [x.value for x in hand.cards if x.value != value]
        kickers.sort(reverse=True)
        kickers = kickers[0:4]
        return {
            "value": value,
            "hand_type": HandOrder.high_card.name,
            "kickers": kickers,
        }

    def check_pair(self, hand):
        """
        Use to check hand for pair, when pairs exist will return dict with
        pair information.  When no pairs exist will return False.

        Params:
            hand: Hand object
        """
        value_array = self.get_value_array(hand.get_hand_matrix())
        max_arg = self.get_max_greater_index(value_array, 1)
        value_array[max_arg] -= 2
        if max_arg is not None:
            max_arg += 2
            return {
                "value": max_arg,
                "hand_type": HandOrder.pair.name,
                "kickers": self.get_kicker(value_array, 3),
            }
        return False

    def check_two_pair(self, hand):
        """
        Use to check a hand for 2 pair, when there is 2 pair will return two
        pair info.  When not will return False.

        Params:
            hand: Hand object
        """

        value_array = self.get_value_array(hand.get_hand_matrix())
        max_arg = self.get_max_greater_index(value_array, 1)
        if max_arg is None:
            return False
        value_array[max_arg] -= 2
        pairs = [max_arg + 2]
        max_arg = self.get_max_greater_index(value_array, 1)
        if max_arg is None:
            return False
        pairs.append(max_arg + 2)
        pairs.sort(reverse=True)
        pairs = tuple(pairs)
        return {"value": pairs, "hand_type": HandOrder.two_pair.name}

    def check_three_of_a_kind(self, hand):
        """
        Use to check a hand for three of a kind, when there is three of a kind
        will return three of a kind info.  When not will return False.

        Params:
            hand: Hand object
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        max_arg = self.get_max_greater_index(value_array, 2)
        if max_arg is not None:
            value_array[max_arg] -= 2
            max_arg = max_arg + 2  # Need to offset value
            return {
                "value": max_arg,
                "hand_type": HandOrder.three_of_a_kind.name,
                "kickers": self.get_kicker(value_array, 2)
            }
        return False

    def check_straight(self, hand):
        """
        Use to check for straight, where there is a straight will return
        straight info. When not will return False.

        Params:
            hand: Hand object
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        high_value = self.check_connected(value_array)
        if high_value:
            return {
                "hand_type": HandOrder.straight.name,
                "value": high_value + 2,
            }
        return False

    def check_flush(self, hand):
        """
        Use to check for flush, where there is a flush will return
        flush info. When not will return False.

        Params:
            hand: Hand object
        """
        hand_matrix = hand.get_hand_matrix()
        suit_array = self.get_suit_array(hand_matrix)
        if np.max(suit_array) >= 5:
            suit_index = np.argmax(suit_array)
            high_card = hand_matrix[suit_index, :]
            high_card = np.argwhere(high_card > 0)
            high_card = max([x[0] for x in high_card]) + 2

            return {"hand_type": HandOrder.flush.name, "value": high_card}
        return False

    def check_full_house(self, hand):
        """
        Use to check for a full house. Will return full house information
        (consiting of a value which is a tuple giving the 3 and 2 cards, in
        that order.) and False if not found.

        Params:
            hand: Hand object representing the hand you are checking for a
                full house.
        """
        value_array = self.get_value_array(hand.get_hand_matrix())
        threes = self.get_max_greater_index(value_array, 2)
        if threes is None:
            return False
        value_array[threes] -= 3
        twos = self.get_max_greater_index(value_array, 1)
        if twos is None:
            return False
        return {
            "hand_type": HandOrder.full_house.name,
            "value": (threes + 2, twos + 2),
        }

    def check_four_of_a_kind(self, hand):
        """
        Use to check a hand for four of a kind, when there is four of a kind
        will return four of a kind info.  When not will return False.

        Params:
            hand: Hand object
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        max_arg = self.get_max_greater_index(value_array, 3)
        if max_arg is not None:
            value_array[max_arg] -= 4
            max_arg = max_arg + 2  # Need to offset value
            return {
                "value": max_arg,
                "hand_type": HandOrder.four_of_a_kind.name,
                "kickers": self.get_kicker(value_array, 1)
            }
        return False

    def check_straight_flush(self, hand):
        """
        Use to check for a straight flush, if found will return the highest
        card in the straight flush. If not will return False.

        Params:
            hand: Hand object
        """
        hand_matrix = hand.get_hand_matrix()
        flush_info = self.check_flush(hand)
        if not flush_info:
            return False
        suit_index = np.argmax(self.get_suit_array(hand_matrix))
        suit_array = hand_matrix[suit_index, :]
        straight_info = self.check_connected(suit_array)
        if straight_info:
            return {
                "hand_type": HandOrder.straight_flush.name,
                "value": straight_info + 2,
            }

        return False

    def get_hand(self, hand):
        """
        Use to get the best hand in a given hand.

        Params:
            hand: Hand object

        """
        for func in [
            self.check_straight_flush,
            self.check_four_of_a_kind,
            self.check_full_house,
            self.check_flush,
            self.check_straight,
            self.check_three_of_a_kind,
            self.check_two_pair,
            self.check_pair,
            self.check_high_card,
        ]:
            info = func(hand)
            if info:
                return info
        return {}

    def compare_hands(self, hand1, hand2):
        hand1_info, hand2_info = self.get_hand(hand1), self.get_hand(hand2)
        if (
            HandOrder[hand1_info["hand_type"]].value
            > HandOrder[hand2_info["hand_type"]].value
        ):
            return "hand1"
        if (
            HandOrder[hand2_info["hand_type"]].value
            > HandOrder[hand1_info["hand_type"]].value
        ):
            return "hand2"
        if hand1_info["hand_type"] == hand2_info["hand_type"]:

            if hand1_info["hand_type"] not in (
                HandOrder.two_pair.name,
                HandOrder.full_house.name,
            ):
                if hand1_info["value"] > hand2_info["value"]:
                    return "hand1"
                if hand2_info["value"] > hand1_info["value"]:
                    return "hand2"

            else:
                hand1_value = hand1_info["value"]
                hand2_value = hand2_info["value"]

                if hand1_value[0] > hand2_value[0]:
                    return "hand1"

                if hand2_value[0] > hand1_value[0]:
                    return "hand2"

                if hand1_value[1] > hand2_value[1]:
                    return "hand1"

                if hand2_value[1] > hand1_value[1]:
                    return "hand2"

        if "kickers" in hand1_info:
            hand1_kickers = hand1_info["kickers"]
            hand2_kickers = hand2_info["kickers"]
            for inx, val in enumerate(hand1_kickers):
                hand2_value = hand2_kickers[inx]

                if val > hand2_value:
                    return "hand1"
                if hand2_value > val:
                    return "hand2"

        return "tie"
