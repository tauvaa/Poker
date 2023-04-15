import random
from enum import Enum

import numpy as np


class Suit(Enum):
    heart = 0
    diamond = 1
    spade = 2
    club = 3


class Card:
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit

    def get_card_matrix(self):
        card_matrix = np.zeros(shape=(4, 13))
        card_matrix[Suit[self.suit].value, self.value - 2] = 1
        return card_matrix

    def __str__(self):
        suit, value = self.suit, self.value
        if value == 11:
            value = "jack"
        elif value == 12:
            value = "queen"
        elif value == 13:
            value = "king"
        elif value == 14:
            value = "ace"
        return f"{value} of {suit}s"



class Deck:
    def __init__(self) -> None:
        self.cards = [
            Card(i, suit)
            for i in range(2, 15)
            for suit in "heart spade diamond club".split()
        ]
    def reset(self):
        self.cards = [
            Card(i, suit)
            for i in range(2, 15)
            for suit in "heart spade diamond club".split()
        ]
        
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)


if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    for card in deck.cards:
        print(card)
