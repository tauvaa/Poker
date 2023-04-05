"""
Functions and classes here are used for storing and checking hand data.
"""
import numpy as np


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
        return {
            "value": max([x.value for x in hand.cards]),
            "hand_type": "high_card",
        }

    def check_pair(self, hand):
        """
        Use to check hand for pair, when pairs exist will return dict with
        pair information.  When no pairs exist will return False.
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        max_arg = np.argwhere(value_array > 1)
        if len(max_arg) > 0:
            max_arg = np.max(max_arg[0]) + 2  # Need to offset value
            return {"value": max_arg, "hand_type": "pair"}
        return False

    def check_two_pair(self, hand):
        """
        Use to check a hand for 2 pair, when there is 2 pair will return two
        pair info.  When not will return False.
        """

        value_array = self.get_value_array(hand.get_hand_matrix())
        pair_info = np.argwhere(value_array > 1)
        if len(pair_info) > 1:
            pairs = [x[0] + 2 for x in pair_info]  # add 2 for the offset
            pairs.sort()
            pairs = tuple(pairs)
            return {"value": pairs, "hand_type": "two_pair"}
        return False

    def check_three_of_a_kind(self, hand):
        """
        Use to check a hand for three of a kind, when there is three of a kind
        will return three of a kind info.  When not will return False.
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        max_arg = np.argwhere(value_array > 2)
        if len(max_arg) > 0:
            max_arg = np.max(max_arg[0]) + 2  # Need to offset value
            return {"value": max_arg, "hand_type": "three_of_a_kind"}
        return False

    def check_straight(self, hand):
        """
        Use to check for straight, where there is a straight will return
        straight info. When not will return False.
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        high_value = self.check_connected(value_array)
        if high_value:
            return {"hand_type": "straight", "value": high_value + 2}
        return False

    def check_flush(self, hand):
        """
        Use to check for flush, where there is a flush will return
        flush info. When not will return False.
        """
        hand_matrix = hand.get_hand_matrix()
        suit_array = self.get_suit_array(hand_matrix)
        if np.max(suit_array) >= 5:
            suit_index = np.argmax(suit_array)
            high_card = hand_matrix[suit_index, :]
            high_card = np.argwhere(high_card > 0)
            high_card = max([x[0] for x in high_card]) + 2

            return {"hand_type": "flush", "value": high_card}
        return False

    def check_four_of_a_kind(self, hand):
        """
        Use to check a hand for four of a kind, when there is four of a kind
        will return four of a kind info.  When not will return False.
        """
        value_array = self.get_value_array(hand.get_hand_matrix())

        max_arg = np.argwhere(value_array > 3)
        if len(max_arg) > 0:
            max_arg = np.max(max_arg[0]) + 2  # Need to offset value
            return {"value": max_arg, "hand_type": "four_of_a_kind"}
        return False

    def check_straight_flush(self, hand):
        hand_matrix = hand.get_hand_matrix()
        flush_info = self.check_flush(hand)
        if not flush_info:
            return False
        suit_index = np.argmax(self.get_suit_array(hand_matrix))
        suit_array = hand_matrix[suit_index, :]
        straight_info = self.check_connected(suit_array)
        if straight_info:
            return {"hand_type": "straight_flush", "value": straight_info + 2}

        return False
