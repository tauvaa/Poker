#!/usr/bin/env python3
import random
import numpy as np
import json
from os.path import join, dirname
from Source.player_choices.examples.player_input import playin_with_yourself
def player1_handle_outcome(game_info):

    with open(join(dirname(__file__),'games_played'), 'a+') as f:
        f.write(json.dumps(game_info))
        f.write(f"\n {''.join(['=' for _ in range(100)])}\n")

# def get_state_cards(cards):
#     cards = cards['cards']
#     if len(cards) == 0:
#         return ''
#     return ' | '.join(cards)

def player1choice(gamestate):
    return playin_with_yourself(gamestate, player='PLAYER 1')
    # #Play player 2.....
    # # print('PLAYER 1')
    # space = ''.join(['\n' for _ in range(5)])
    # print(f"{10*space}DECISION PLAYER 1")
    # player_info = gamestate['player_info']
    # betting_info = gamestate['betting_info']
    # flop = player_info['flop']
    # turn = player_info['turn']
    # river = player_info['river']
    # player_cards = player_info['hand']
    # state_strings = zip(('player_cards flop turn river'.split()),[get_state_cards(x) for x in (player_cards, flop, turn, river)])
    # for state, string in state_strings:
    #     if len(string) > 0:
    #         print(f'{state}: {string}')
    # to_call = betting_info['to_call']
    # prev_choice = betting_info['previous_choice']
    # print(f'to call: {to_call} previous choice: {prev_choice}')
    # to_ret = input(f"what do you want to do, options: {' '.join(betting_info['betting_options'])}{space}")
    #
    # if 'bet' in to_ret:
    #     to_ret = to_ret.split()
    #     if len(to_ret) == 1: to_ret.append(25)
    #     return {'choice': to_ret[0], 'amount': int(to_ret[1])}
    # return {'choice': to_ret}
    #
    #
    # hand_matrix = player_info['hand']['hand_matrix']
    # if np.max(np.matmul(hand_matrix, np.ones(13))) >1 and 'bet' in gamestate['betting_info']['betting_options']:
    #     return {'choice': 'bet', 'amount': 25}
    # else:
    #     if 'call' in gamestate['betting_info']['betting_options']:
    #         return {'choice': 'call'}
    # options = gamestate['betting_info']['betting_options']
    # choice = {'choice': random.choice(options)}
    # if choice['choice'] == 'bet':
    #     choice['amount']=25
    # return choice