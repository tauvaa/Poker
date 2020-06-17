#!/usr/bin/env python3

from Source.hands import Deck, Card
from Source.player import Player
from Source.game import Game, Flop, River, Turn, play
class StackedDeck(Deck):
    def __init__(self):
        super(StackedDeck,self).__init__()
    def card_swap(self, index1, index2):
        """
        replace card at index1 with card at index2
        :param index1:
        :param index2:
        :return:
        """
        temp = self.cards[index1]
        self.cards[index1] = self.cards[index2]
        self.cards[index2] = temp
    def stack(self, stacked_card, stack_ind):
        for ind, card in enumerate(self.cards):
            if card.value == stacked_card.value and card.suit == stacked_card.suit:
                self.card_swap(stack_ind, ind)


class Cheating(Game):
    def __init__(self, player1, player2):
        super(Cheating, self).__init__(player1, player2)

    def new_hand(self, deck=None):
        self.winner = None
        self.print_player_pots()
        self.player1.reset_hand()
        self.player2.reset_hand()
        self.switch_dealer()
        self.game_count += 1
        if self.game_count % 500 == 0:
            self.small_blind = 2*self.small_blind
            self.big_blind = 2*self.big_blind
            print(self.big_blind, self.small_blind)
        if deck is None:
            self.deck = Deck() # re-initalize deck
            self.deck.shuffle()
        else:
            self.deck=deck
        assert len(self.deck.cards) == 52
        self.pot = 0
        self.state = 'preflop'
        self.flop = Flop()
        self.turn = Turn()
        self.river = River()
        self.player1_betting = self.player1.is_dealer
    def play_hand(self, deck=None):
        print(''.join(['+' for _ in range(10)]+['new game'] + ['+' for _ in range(10)]))

        self.new_hand(deck)
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
# player1choice = lambda x: {'choice':'check'}
# player2choice = lambda x: {'choice':'check'}

def play_games(n_games=10, player1_hand=[], player2_hand=[], flop=[],turn=[],river=[]):
    counter = {}
    for _ in range(n_games):
        game = Cheating(Player('player1'), Player('player2'))
        deck = StackedDeck()
        deck.shuffle()

        for card, ind in zip(player1_hand,range(50,50-2*len(player1_hand),-2)):

            deck.stack(card,ind)
            print(ind)
        for card, ind in zip(player2_hand, range(51, 51 - 2 * len(player2_hand), -2)):
            print(ind)
            deck.stack(card, ind)
        ind=47
        for card in flop + turn + river:
            deck.stack(card,ind)

            print(ind, card.card_string())
            ind -= 1
        # for k in deck.cards:
        #     print(k.card_string())
        # player 2
        # deck.stack(Card('Diamonds', 14),51)
        # deck.stack(Card('Hearts', 14),49)
        # player 1
        # deck.stack(Card('Spades', 9), 50)
        # deck.stack(Card('Spades', 8), 48)
        game.play_hand(deck)
        if game.winner.player_name in counter:
            counter[game.winner.player_name] += 1
        else:
            counter[game.winner.player_name] = 1

    return counter

def get_stats(dic):
    total = sum(dic[k] for k in dic)
    for x in dic:
        print(f'{x}: {dic[x]/total}')

if __name__ == '__main__':
    x = play_games(n_games=1000
                   ,player1_hand=[Card('Hearts', 11), Card('Diamonds', 11)]
                   ,player2_hand=[Card('Clubs', 9), Card('Clubs',8)]
                   # ,flop=[Card('Spades',x) for x in (12,13,14)]
                   # ,turn =[Card('Clubs', 14)]
                   # ,river=[Card('Clubs', 10)]
                   )
    get_stats(x)