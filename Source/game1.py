#!/usr/bin/env python3
from Source.hands import HandMatrix, Deck
from Source.player import Player
from config import starting_big_blind, starting_small_blind
from Source.player_choices.player1 import player1choice
from Source.player_choices.player2 import player2choice

class Betting:
    """used to update game... probably better if this extended game"""

    def __init__(self, game):
        self.game = game
        self.is_player1_betting = (not game.player1.is_dealer)
        self.previous_bet = None
        self.to_call = 0

    def switch_bidder(self):
        self.is_player1_betting = not self.is_player1_betting

    def get_betting_info(self):
        pass

    def choice(self):
        info = {'betting_info': self.get_betting_info()}

        if self.is_player1_betting:
            info['player_info'] = self.game.get_player1_info()
            decision = player1choice(info)

        else:
            info['player_info'] = self.game.get_player2_info()
            decision = player2choice(info)

    def gamble(self):
        return self.choice()

    def check(self):
        pass

    def call(self):
        pass

    def bet(self, amount):
        pass

    def fold(self):
        pass

class Flop(HandMatrix):
    def __init__(self):
        super(Flop, self).__init__()

class Turn(HandMatrix):
    def __init__(self):
        super(Turn, self).__init__()

class River(HandMatrix):
    def __init__(self):
        super(River, self).__init__()


class Game:
    def __init__(self, player1, player2):
        self.game_count = 0
        self.player1 = player1
        self.player2 = player2
        self.player2.switch_dealer()
        self.small_blind = starting_small_blind
        self.big_blind = starting_big_blind
        self.pot = 0
        self.deck = None
        self.flop = None
        self.turn = None
        self.river = None
        self.state = None
        self.player1_betting = None

    def new_hand(self):
        self.switch_dealer()
        self.game_count += 1
        self.deck = Deck() # re-initalize deck
        self.deck.shuffle()
        assert len(self.deck.cards) == 52
        self.pot = 0
        self.state = 'preflop'
        self.flop = Flop()
        self.turn = Turn()
        self.river = River()
        self.player1_betting = (not self.player1.is_dealer)

    def switch_dealer(self):
        self.player1.is_dealer = not self.player1.is_dealer
        self.player2.is_dealer = not self.player2.is_dealer

    def update_pot(self, amount):
        if amount < 0:
            raise ValueError("can't steal from the pot")
        self.pot += amount

    def get_blinds(self):
        if self.player1.is_dealer:
            # small blind
            self.player1.update_bank(-1*self.small_blind)
            # big blind
            self.player2.update_bank(-1*self.big_blind)

        else:
            self.player1.update_bank(-1 * self.big_blind)
            self.player2.update_bank(-1 * self.small_blind)
        self.update_pot(self.small_blind + self.big_blind)

    def _deal_community_card(self):
        card = self.deck.deal_card()
        if self.state == 'flop':
            self.flop.add_card(card)
        elif self.state == 'turn':
            self.turn.add_card(card)
        elif self.state == 'river':
            self.river.add_card(card)

    def _start_hand(self):
        # get the blinds
        self.get_blinds()
        if self.player1.is_dealer:
            for _ in range(2):
                self.player2.add_card(self.deck.deal_card())
                self.player1.add_card(self.deck.deal_card())
        else:
            for _ in range(2):
                self.player1.add_card(self.deck.deal_card())
                self.player2.add_card(self.deck.deal_card())

    def switch_state(self):
        possible_states = ['preflop', 'flop', 'turn', 'river', 'show_cards']
        self.state = possible_states[possible_states.index(self.state) + 1]

    def _flop(self):
        for _ in range(3):
            self._deal_community_card()

    def _turn(self):
        pass
    def _river(self):
        pass
    def bet(self):
        self._print_game_state()
        b = Betting(self)
        b.bet(self)
    def play_hand(self):
        self.new_hand()
        self._start_hand()
        self.bet()
        self._flop()
        self.bet()
        self._turn()
        self.bet()
        self._river()
        self.bet()

    def _print_game_state(self):
        game_state = {'player_1_state':self.player1.get_player_state(),
                      'player_2_state':self.player2.get_player_state()}
        print(game_state)

def play_hand(game=None):
    if game is None:
        player1 = Player('player 1')
        player2 = Player('player 2')
        game = Game(player1, player2)
    game.play_hand()
    # game._start_hand()
    # b = Betting(game)
    # b.bet()
    # game._turn()
    # b = Betting(game)
    # b.bet()

    print(game.state)

    # print(game.flop.hand_matrix)
    # print(game.pot)
    # for x in player1.cards: print(x.card_string())
    # print(game.player2.check_cards())
if __name__ == '__main__':
    play_hand()