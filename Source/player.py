#!/usr/bin/env python3

from Source.hands import Hand, HandMatrix, Deck
from config import starting_big_blind, starting_small_blind, starting_bank


class Player(Hand):
    def __init__(self, player_name, bank=starting_bank, to_print=True):
        super(Player, self).__init__()
        self.player_name = player_name
        self.bank = bank
        self.is_dealer = False
        self.to_print = to_print
        self.bets = []
    
    def reset_bets(self):
        self.bets = []

    def switch_dealer(self):
        self.is_dealer = not self.is_dealer

    def check_cards(self):
        return self.hand_matrix

    def update_bank(self, amount):
        self.bank += amount

    def print_hand(self):
        if self.to_print:
            sep_car = ' | '
            return sep_car.join([x.card_string() for x in self.cards])

    def get_player_state(self):
        player_state = dict(hand=dict(cards=[x.card_string() for x in self.cards],
                            hand_matrix=self.hand_matrix.copy()),
                            bank=self.bank,
                            bets=self.bets
                            )
        return player_state.copy()

    # d = Deck()
    # d.shuffle()
    # for x in d.cards:
    #     print(x.card_string())
