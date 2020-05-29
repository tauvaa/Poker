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
        self.previous_choice = None
        self.to_call = 0

    def switch_bidder(self):
        self.is_player1_betting = not self.is_player1_betting

    def get_betting_info(self):
        betting_options = ['fold', 'call', 'raise']
        if self.previous_choice is None or self.previous_choice == 'check':
            betting_options.append('check')
        betting_info = dict(
            previous_previous_choice=self.previous_choice,
            to_call=self.to_call,
            betting_options=betting_options
        )
        return betting_info
    def ask_player(self):
        info = {'betting_info': self.get_betting_info()}
        if self.is_player1_betting:
            info['player_info'] = self.game.get_player_info(self.game.player1)
            decision = player1choice(info)

        else:
            info['player_info'] = self.game.get_player_info(self.game.player2)
            decision = player2choice(info)
        return decision
    def choice(self):
        decision = self.ask_player()

        if decision['choice'] == 'check':
            if self.previous_choice == 'check' or self.previous_choice is None:
                return self.check()
            else:
                # you couldn't check in that situation
                return self.fold()
        elif decision['choice'] == 'bet':
            if 'amount' not in decision:
                return self.fold()
            else:
                return self.bet(decision['amount'])
        elif decision['choice'] == 'call':
            return self.call()
        else:
            return self.fold()

    def gamble(self):
        self.game.switch_state()
        return self.choice()


    def check(self):
        if self.previous_choice == 'check':
            return False
        else:
            self.previous_choice = 'check'
            self.switch_bidder()
            return self.choice()

    def call(self):
        if self.is_player1_betting:
            self.game.update_pot(self.to_call, self.game.player1)
        else:
            self.game.update_pot(self.to_call, self.game.player2)
        if self.to_call == 0:
            return self.check()
        else:
            return False

    def bet(self, amount):
        if self.is_player1_betting:
            self.game.update_pot(amount=amount, player=self.game.player1)
        else:
            self.game.update_pot(amount=amount, player=self.game.player2)
        self.to_call = amount
        self.previous_choice = 'bet'
        self.switch_bidder()
        return self.choice()


    def fold(self):
        if self.is_player1_betting:
            self.game.update_pot(-1*self.game.pot, self.game.player2)
        else:
            self.game.update_pot(-1*self.game.pot, self.game.player1)
        return True

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

    def get_game_info(self):
        flop_cards = [x.card_string() for x in self.flop.cards]
        turn_cards = [x.card_string() for x in self.turn.cards] # list with 1 elm
        river_cards = [x.card_string() for x in self.river.cards] # list with 1 elm
        flop = dict(matrix=self.flop.get_hand_matrix(), cards=flop_cards)
        turn = dict(matrix=self.turn.get_hand_matrix(), cards=turn_cards)
        river = dict(matrix=self.river.get_hand_matrix(), cards=river_cards)
        return {'flop': flop,
                'turn': turn,
                'river': river,
                'pot': self.pot}
    def get_player_info(self, player):
        player_info = {**self.get_game_info().copy(), **player.get_player_state()}
        return player_info

    def new_hand(self):

        self.player1.reset_hand()
        self.player2.reset_hand()
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

    def update_pot(self, amount, player):
        self.pot += amount
        player.bank -= amount

    def get_blinds(self):
        if self.player1.is_dealer:
            self.update_pot(self.small_blind, self.player1)
            self.update_pot(self.big_blind, self.player2)
        else:
            self.update_pot(self.small_blind, self.player2)
            self.update_pot(self.big_blind, self.player1)

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
        self._deal_community_card()

    def _river(self):
        self._deal_community_card()

    def bet(self):
        # self._print_game_state()
        b = Betting(self)
        is_fold = b.gamble()
        return is_fold

    def showdown_add_cards(self, list_cards):
        for card in list_cards:
            self.player2.add_card(card)
            self.player1.add_card(card)

    def showdown(self):
        """see who won"""
        # ====================================================================================
        #                               DRAW IS HERE!!!!!!
        # ====================================================================================
        def draw():
            # print(self.player1_info)
            if self.player1_info['hand'] =='high card':
                if self.player1_info['high_card']>self.player2_info['high_card']:
                    return 'player1'
                elif self.player1_info['high_card']<self.player2_info['high_card']:
                    return 'player2'

            elif self.player1_info['hand'] == 'pair':
                if self.player1_info['info']['hc'] > self.player2_info['info']['hc']:
                    return 'player1'
                elif self.player1_info['info']['hc'] < self.player2_info['info']['hc']:
                    return 'player2'

            return 'draw'

        ranking = [
            'straight flush'
            , 'four of a kind'
            , 'full house'
            , 'regular flush'
            , 'straight'
            , 'three of a kind'
            , 'two pair'
            , 'pair'
            , 'high card'
        ]
        try:
            player1_info = self.player1.check_hand()
            player2_info = self.player2.check_hand()
        except Exception as err:
            import traceback
            import sys
            print("player 1")
            for c in self.player1.cards:
                print(c.card_string())
            print("player 2")
            for c in self.player2.cards:
                print(c.card_string())
            print(traceback.print_exc(file=sys.stdout))
            raise err
        self.player1_info = player1_info
        self.player2_info = player2_info
        # self.print_board()
        if ranking.index(player1_info['hand']) < ranking.index(player2_info['hand']):
            return 'player1'
        elif ranking.index(player1_info['hand']) > ranking.index(player2_info['hand']):
            return 'player2'
        else:
            return draw()
    def print_board(self):
        sep_char = ' | '
        flop_string = sep_char.join([x.card_string() for x in self.flop.cards])
        turn_string = sep_char.join([x.card_string() for x in self.turn.cards])
        river_string = sep_char.join([x.card_string() for x in self.river.cards])
        board = sep_char.join(['board: ', flop_string, turn_string, river_string])
        player1_string = sep_char.join(['player 1: '] +[x.card_string() for x in self.player1.cards])
        player2_string = sep_char.join(['player 2: '] + [x.card_string() for x in self.player2.cards])
        print(''.join(['=' for _ in range(100)]))
        print(board)
        print(player1_string)
        print(player2_string)


    def play_hand(self):
        print(''.join(['+' for _ in range(10)]+['new game'] + ['+' for _ in range(10)]))
        self.new_hand()
        self._start_hand()
        is_fold = self.bet()
        if not is_fold:
            self._flop()
            is_fold = self.bet()
        if not is_fold:
            self._turn()
            self.bet()
        if not is_fold:
            self._river()
            is_fold = self.bet()
        if not is_fold:
            # add the community cards to the players hands

            for list_cards in (self.flop.cards, self.turn.cards, self.river.cards):
                self.showdown_add_cards(list_cards)
            winner = self.showdown()
            if winner == 'player1':
                self.update_pot(-1*self.pot, self.player1)
            elif winner == 'player2':
                self.update_pot(-1*self.pot, self.player2)
            elif winner == 'draw':
                draw_pot = self.pot
                self.update_pot(-1*draw_pot/2, self.player1)
                self.update_pot(-1*draw_pot/2, self.player2)
            print(winner)
            print(f'player 1: {self.player1_info}')
            print(f'player 2: {self.player2_info}')
            self.print_board()
    def _print_game_state(self):
        # SEEMS USELESS
        game_state = {'player_1_state':self.player1.get_player_state(),
                      'player_2_state':self.player2.get_player_state()}
        print(game_state)

def play(game=None):
    if game is None:
        player1 = Player('player 1')
        player2 = Player('player 2')
        game = Game(player1, player2)
    while True:
        if game.player1.bank <=0:
            return 'player 1 loses'
        if game.player2.bank <= 0:
            return 'player 2 loses'

        game.play_hand()



if __name__ == '__main__':
    x = play()
    print(x)