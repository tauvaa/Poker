#!/usr/bin/env python3

from Source.hands import Hand, HandMatrix, Deck
from config import starting_big_blind, starting_small_blind


class Player(Hand):
    def __init__(self, player_name, bank=1000):
        super(Player, self).__init__()
        self.player_name = player_name
        self.bank = bank
        self.is_dealer = False

    def switch_dealer(self):
        self.is_dealer = not self.is_dealer

    def check_cards(self):
        return self.hand_matrix

    def update_bank(self, amount):
        self.bank += amount

    def get_player_state(self):
        player_state = dict(cards=[x.card_string() for x in self.cards],
                            hand_matrix=self.hand_matrix,
                            bank=self.bank
                            )
        return player_state.copy()

    # d = Deck()
    # d.shuffle()
    # for x in d.cards:
    #     print(x.card_string())
