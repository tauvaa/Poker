#!/usr/bin/env python3
from Source.hands import HandMatrix, Deck
from Source.player import Player
from config import starting_big_blind, starting_small_blind
from Source.player_choices.player1.player1 import player1choice, player1_handle_outcome
from Source.player_choices.player2.player2 import player2choice, player2_handle_outcome

class Betting:
    """used to update game... probably better if this extended game"""

    def __init__(self, game):
        self.game = game
        self.is_player1_betting = (not game.player1.is_dealer)
        self.previous_choice = None
        self.to_call = 0
        if self.game.state =='preflop':
            self.to_call = self.game.big_blind - self.game.small_blind

        self.betting_options = None

    def switch_bidder(self):
        self.game.print_player_pots()
        self.is_player1_betting = not self.is_player1_betting

    def get_betting_info(self):
        betting_options = ['fold']
        if self.to_call > 0:
            betting_options.append('call')
        if self.game.player1.bank > 0 and self.game.player2.bank >0:
            if self.is_player1_betting and self.game.player1.bank > self.to_call:
                betting_options.append('bet')
            elif not self.is_player1_betting and self.game.player2.bank > self.to_call:
                betting_options.append('bet')
        if self.previous_choice is None or self.previous_choice == 'check':
            betting_options.append('check')
        print(betting_options)
        self.betting_options = betting_options
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
        if decision['choice'] not in self.betting_options:
            return self.fold()

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
                if self.is_player1_betting:
                    self.game.update_pot(self.to_call, self.game.player1)
                else:
                    self.game.update_pot(self.to_call, self.game.player2)
                self.to_call = 0
                amount = decision['amount']
                if amount > min(self.game.player1.bank, self.game.player2.bank):
                    amount = min(self.game.player1.bank, self.game.player2.bank)
                return self.bet(amount)
        elif decision['choice'] == 'call':
            return self.call()
        else:
            return self.fold()

    def gamble(self):
        # self.game.switch_state()
        return self.choice()


    def check(self):
        if self.is_player1_betting:
            if self.game.player1.to_print:
                print(f'{self.game.player1.player_name}: checked')
        else:
            if self.game.player2.to_print:
                print(f'{self.game.player2.player_name}: checked')
        if self.previous_choice == 'check':
            return False
        else:
            self.previous_choice = 'check'
            self.switch_bidder()
            return self.choice()

    def call(self):
        if self.is_player1_betting:
            self.game.update_pot(self.to_call, self.game.player1)
            if self.game.player1.to_print and self.to_call > 0 :
                print(f'{self.game.player1.player_name}: called {self.to_call}')
        else:
            self.game.update_pot(self.to_call, self.game.player2)
            if self.game.player2.to_print and self.to_call > 0 :
                print(f'{self.game.player2.player_name}: called {self.to_call}')
        if self.to_call == 0:
            return self.check()
        else:
            return False

    def bet(self, amount):
        if amount < 0:
            self.game.print_player_pots()
            raise ValueError
        if self.is_player1_betting:
            self.game.update_pot(amount=amount, player=self.game.player1)
            if self.game.player1.to_print:
                print(f'{self.game.player1.player_name}: bet {amount}')
        else:
            self.game.update_pot(amount=amount, player=self.game.player2)
            if self.game.player2.to_print:
                print(f'{self.game.player2.player_name}: bet {amount}')
        self.to_call = amount - self.to_call
        self.previous_choice = 'bet'
        self.switch_bidder()
        return self.choice()


    def fold(self):
        if self.is_player1_betting:
            if self.game.player1.to_print:
                print(f'{self.game.player1.player_name}: folds')
            self.game.update_pot(-1*self.game.pot, self.game.player2)
            self.game.winner = self.game.player2

        else:
            if self.game.player2.to_print:
                print(f'{self.game.player2.player_name}: folds')
            self.game.update_pot(-1*self.game.pot, self.game.player1)
            self.game.winner = self.game.player1

        return True

class GameStates(HandMatrix):
    def __init__(self, state_name=None, to_print=True):
        super(GameStates, self).__init__()
        self.state_name = state_name
        self.to_print = to_print
    def print_state(self):
        if self.to_print:
            if self.state_name is not None:
                wrapper = ''.join(['=' for _ in range(10)])
                print(3*wrapper)
                print(f'{wrapper} {self.state_name} {wrapper}')
                print(3*wrapper)
            splt_ch = ' | '
            print(splt_ch.join([x.card_string() for x in self.cards]))


class Flop(GameStates):
    def __init__(self):
        super(Flop, self).__init__()
        self.state_name = 'Flop'
class Turn(GameStates):
    def __init__(self):
        super(Turn, self).__init__()
        self.state_name = 'Turn'
class River(GameStates):
    def __init__(self):
        super(River, self).__init__()
        self.state_name = 'River'

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
        self.winner = None
        self.pot_total = 0

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
                'pot': self.pot
                ,'state': self.state}
    def get_player_info(self, player):
        player_info = {**self.get_game_info().copy(), **player.get_player_state()}
        return player_info

    def print_player_pots(self):
        print(f"player 1 bank: {self.player1.bank}")
        print(f'player 2 bank: {self.player2.bank}')

    def new_hand(self):
        if self.winner is not None and self.winner.player_name == 'player 2':
            with open('p2w.txt', 'a+') as f:
                f.write('player2\n')

        self.winner = None
        self.print_player_pots()
        self.player1.reset_hand()
        self.player2.reset_hand()
        self.switch_dealer()
        self.game_count += 1
        if self.game_count % 50 == 0:
            self.small_blind = 3*self.small_blind
            self.big_blind = 3*self.big_blind
            print(self.big_blind, self.small_blind)
        self.deck = Deck() # re-initalize deck
        self.deck.shuffle()
        assert len(self.deck.cards) == 52
        self.pot = 0
        self.state = 'preflop'
        self.flop = Flop()
        self.turn = Turn()
        self.river = River()
        self.player1_betting = self.player1.is_dealer

    def switch_dealer(self):
        self.player1.switch_dealer()
        self.player2.switch_dealer()

    def update_pot(self, amount, player):
        if amount < 0:
            self.pot_total = self.pot
            print(f'moved: {-1*amount} to {player.player_name}')
        self.pot += amount
        player.bank -= amount


    def get_blinds(self):
        # self.pre_bet_action = self.big_blind - self.small_blind
        if self.player1.is_dealer:
            if self.player1.bank < self.small_blind:
                self.update_pot(self.player1.bank, self.player1)
            else:
                self.update_pot(self.small_blind, self.player1)
            if self.player2.bank < self.big_blind:
                self.update_pot(self.player2.bank, self.player2)
            else:
                self.update_pot(self.big_blind, self.player2)
        else:
            if self.player2.bank < self.small_blind:
                self.update_pot(self.player2.bank, self.player2)
            else:
                self.update_pot(self.small_blind, self.player2)
            if self.player1.bank < self.big_blind:
                self.update_pot(self.player1.bank, self.player1)
            else:
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
        for x in (self.player1, self.player2):
            if x.to_print:
                print(f'{x.player_name}: {x.print_hand()}')

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

    def draw(self):
        # print(self.player1_info)
        if self.player1_info['hand'] =='high card':
            if self.player1_info['high_card']>self.player2_info['high_card']:
                return self.player1
            elif self.player1_info['high_card']<self.player2_info['high_card']:
                return self.player2

        elif self.player1_info['hand'] == 'pair':
            if self.player1_info['info']['hc'] > self.player2_info['info']['hc']:
                return self.player1
            elif self.player1_info['info']['hc'] < self.player2_info['info']['hc']:
                return self.player2

        return Player('draw')

    def showdown(self):
        """see who won"""
        # ====================================================================================
        #                               DRAW IS HERE!!!!!!
        # ====================================================================================

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
            self.winner = self.player1
        elif ranking.index(player1_info['hand']) > ranking.index(player2_info['hand']):
            self.winner = self.player2
        else:
            self.winner = self.draw()

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

    def end_game(self, is_fold):
        """used to get the end of game info, tells winner, win type (fold/not show_cards) and opponnent cards
        if found here.  This gets passed to the player handle outcome functions"""
        if self.player1.is_dealer:
            dealer = self.player1.player_name
        elif self.player2.is_dealer:
            dealer = self.player2.player_name
        base_game_info = {
            'winner': self.winner.player_name,
            'is_fold': is_fold,
            'player_1_bank': self.player1.bank,
            'player_2_bank': self.player2.bank,
            'pot_size': self.pot_total,
            'blinds':{'small_blind':self.small_blind, 'big_blind':self.big_blind},
            'dealer': dealer

        }
        self.pot_total = 0
        if is_fold or True: # change this to add more info for non fold games
            player1_handle_outcome(game_info=base_game_info.copy())
            player2_handle_outcome(game_info=base_game_info.copy())

    # ================================================================================================================
    # ==========================================   HAND STUFF  =======================================================
    # ================================================================================================================
    def play_hand(self):
        print(''.join(['+' for _ in range(10)]+['new game'] + ['+' for _ in range(10)]))
        self.new_hand()
        self._start_hand()
        is_fold = self.bet()
        # =========================== FLOP ===========================
        if not is_fold:
            self.switch_state()
            self.player1_betting = not self.player1_betting  # after opening betting switch so dealer doesn't bet first
            self._flop()
            self.flop.print_state()
            is_fold = self.bet()
        # =========================== TURN ===========================
        if not is_fold:
            self.switch_state()
            self._turn()
            self.turn.print_state()
            is_fold = self.bet()
        # =========================== RIVER ===========================
        if not is_fold:
            self.switch_state()
            self._river()
            self.river.print_state()
            is_fold = self.bet()
        # =========================== SHOWDOWN ===========================
        if not is_fold:
            self.switch_state()
            # add the community cards to the players hands
            for list_cards in (self.flop.cards, self.turn.cards, self.river.cards):
                self.showdown_add_cards(list_cards)
            self.showdown()
            if self.winner.player_name != 'draw':
                self.update_pot(-1*self.pot, self.winner)
            else:
                draw_pot = self.pot
                self.update_pot(-1 * draw_pot / 2, self.player1)
                self.update_pot(-1 * draw_pot / 2, self.player2)


            print(f'player 1: {self.player1_info}')
            print(f'player 2: {self.player2_info}')
            self.print_board()
        self.end_game(is_fold)


def play(game=None):
    if game is None:
        player1 = Player('player 1')
        player2 = Player('player 2')
        game = Game(player1, player2)
    while True:
        if game.player1.bank <=0:
            return game.player2.player_name
        if game.player2.bank <= 0:
            return game.player1.player_name

        game.play_hand()



if __name__ == '__main__':
    x = play()
    # print(x)