from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Union

from src.player import Player
from src.utils.betting import BetOption
from src.utils.deck import Card, Deck
from src.utils.hand import HandChecker


class GamePhase(Enum):
    preflop = auto()
    flop = auto()
    turn = auto()
    river = auto()
    check_cards = auto()


@dataclass
class GameState:
    pot: Union[float, int]
    bet_amount: Union[float, int, None]
    player: Player
    opponent: Player
    community_cards: Union[List[Card], None]
    winner: Union[Player, None]
    loser: Union[Player, None]
    dealer: Player
    game_phase: GamePhase


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
        self.game_phase = GamePhase.preflop
        self.deck = Deck()
        self.pot = Pot()
        self.community_cards = []
        self.small_blind = 25
        self.big_blind = 50
        self.winner = None
        self.loser = None
        self.hand_checker = HandChecker()
        self.hands_checked = False

    def deal_card(self, player):
        card = self.deck.deal_card()
        player.add_card(card)

    def betting(self):
        """Use to simulate betting."""
        bet_index = 0
        num_checks = 0
        bet_amount = 0
        bet_options = [BetOption.check, BetOption.bet, BetOption.fold]
        first_bet = False

        if self.dealer == self.player1:
            bettors = [self.player2, self.player1]

        else:
            bettors = [self.player1, self.player2]
        if self.game_phase == GamePhase.preflop:
            bettors.reverse()
            bet_amount = self.big_blind - self.small_blind
            bet_options = [BetOption.call, BetOption.bet, BetOption.fold]

        while True:
            bettor = bettors[bet_index % len(bettors)]
            bet_index += 1
            opponent = bettors[bet_index % len(bettors)]
            game_state = self.get_game_state(bettor, opponent, bet_amount)
            decision = bettor.decision(
                bet_amount, bet_options, game_info=game_state
            )

            if decision.choice == BetOption.fold:

                self.loser = bettor
                winner = bettors[bet_index % len(bettors)]
                self.winner = winner

                return False

            if decision.choice == BetOption.call:
                bettor.update_bank(-bet_amount)
                self.pot.add_pot(bet_amount)
                if self.game_phase != GamePhase.preflop or first_bet:

                    return True
                first_bet = True
                bet_options = [BetOption.check, BetOption.bet]
                num_checks += 1

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

    def get_game_state(self, player, opponent, bet_amount):
        game_state = GameState(
            pot=self.pot.amount,
            bet_amount=bet_amount,
            player=player,
            opponent=opponent,
            community_cards=self.community_cards,
            winner=self.winner,
            loser=self.loser,
            dealer=self.dealer,
            game_phase=self.game_phase,
        )
        return game_state

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
        self.dealer = (
            self.player2 if self.dealer == self.player1 else self.player1
        )
        # Display the results
        players = [self.player1, self.player2]
        for i, player in enumerate(players):
            if player.display:
                opponent = players[(i + 1) % 2]
                game_info = self.get_game_state(player, opponent, None)
                player.display.show(game_info)
        self.pot.reset()
        self.player1.hand.reset()
        self.player2.hand.reset()
        self.deck.reset()
        self.community_cards = []
        self.game_phase = GamePhase.preflop
        self.winner = None
        self.loser = None
        self.hands_checked = False

    def check_hands(self):
        """
        Use to check hands of player1 and player2 and assign a winner.
        """
        self.hands_checked = True
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
        self.game_phase = GamePhase.flop
        if not self.flop():
            self.new_hand()
            return
        self.game_phase = GamePhase.turn
        if not self.turn():
            self.new_hand()
            return
        self.game_phase = GamePhase.river
        if not self.river():
            self.new_hand()
            return
        self.game_phase = GamePhase.check_cards
        self.check_hands()
        winner = self.winner
        self.new_hand()
        return winner
