from enum import Enum, auto

from src.player import Player
from src.utils.betting import BetOption
from src.utils.deck import Card, Deck
from src.utils.hand import HandChecker


class GameState(Enum):
    preflop = auto()
    flop = auto()
    turn = auto()
    river = auto()


class Pot:
    def __init__(self):
        self.amount = 0

    def add_pot(self, amount):
        self.amount += amount

    def reset(self):
        self.amount = 0


class Game:
    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2
        self.dealer = self.player1
        self.game_state = GameState.preflop
        self.deck = Deck()
        self.pot = Pot()
        self.community_cards = []
        self.small_blind = 25
        self.big_blind = 50
        self.winner = None
        self.loser = None
        self.hand_checker = HandChecker()

    def deal_card(self, player):
        card = self.deck.deal_card()
        player.add_card(card)

    def betting(self):
        """Use to simulate betting."""
        bet_index = 0
        num_checks = 0
        bet_amount = 0
        bet_options = [BetOption.check, BetOption.bet, BetOption.fold]
        if self.dealer == self.player1:
            bettors = [self.player2, self.player1]
        else:
            bettors = [self.player1, self.player2]

        while True:
            bettor = bettors[bet_index % len(bettors)]
            bet_index += 1
            decision = bettor.decision(bet_amount, bet_options)

            if decision.choice == BetOption.fold:

                self.loser = bettor
                winner = bettors[bet_index % len(bettors)]
                self.winner = winner

                return False

            if decision.choice == BetOption.call:
                bettor.update_bank(-bet_amount)
                self.pot.add_pot(bet_amount)
                return True

            if decision.choice == BetOption.check:
                if num_checks == 1:
                    return True
                num_checks += 1

            if decision.choice == BetOption.bet:
                bettor.update_bank(-(bet_amount + decision.bet_amount))
                self.pot.add_pot(bet_amount + decision.bet_amount)
                bet_amount = decision.bet_amount
                num_checks = 0
                bet_options = [BetOption.call, BetOption.bet, BetOption.fold]

    def deal_comunity_cards(self, num_cards):
        player_order = [self.player2, self.player1]
        if self.dealer == self.player2:
            player_order = [self.player1, self.player2]
        for _ in range(num_cards):
            card = self.deck.deal_card()
            self.community_cards.append(card)
            for player in player_order:
                player.add_card(card)

    def preflop(self):
        # deal cards

        self.deck.shuffle()
        if self.dealer == self.player1:

            # blinds
            self.player2.update_bank(-self.small_blind)
            self.pot.add_pot(self.small_blind)

            self.player1.update_bank(-self.big_blind)
            self.pot.add_pot(self.big_blind)
            # deal cards
            for _ in range(2):
                self.deal_card(self.player2)
                self.deal_card(self.player1)
        else:
            for _ in range(2):
                self.deal_card(self.player1)
                self.deal_card(self.player2)
        return self.betting()

    def flop(self):
        # burn
        self.deck.deal_card()

        self.deal_comunity_cards(3)
        return self.betting()

    def turn(self):
        # burn
        self.deck.deal_card()

        self.deal_comunity_cards(1)
        return self.betting()

    def river(self):
        # burn
        self.deck.deal_card()

        self.deal_comunity_cards(1)
        return self.betting()

    def new_hand(self):
        """
        Use to reset hand after a player wins. Need to transfer pot, switch
        dealers and reset cards.
        """
        if self.winner is not None:
            self.winner.update_bank(self.pot.amount)
        else:
            self.player1.update_bank(self.pot.amount / 2)
            self.player2.update_bank(self.pot.amount / 2)
        self.pot.reset()
        self.dealer = (
            self.player1 if self.dealer == self.player2 else self.player1
        )
        self.player1.hand.reset()
        self.player2.hand.reset()
        self.community_cards = []
        self.game_state = GameState.preflop
        self.winner = None
        self.loser = None

    def check_hands(self):
        """
        Use to check hands of player1 and player2 and assign a winner.
        """
        winner = self.hand_checker.compare_hands(
            self.player1.hand, self.player2.hand
        )
        if winner == "hand1":
            self.winner = self.player1
        if winner == "hand2":
            self.winner = self.player2

    def play_hand(self):
        """
        Use to play a single hand.
        """
        if not self.preflop():
            self.new_hand()
            return
        self.game_state = GameState.flop
        if not self.flop():
            self.new_hand()
            return
        self.game_state = GameState.turn
        if not self.turn():
            self.new_hand()
            return
        self.game_state = GameState.river
        if not self.river():
            self.new_hand()
            return
        self.check_hands()
        self.new_hand()
