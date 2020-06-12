#!/user/bin/env python3
import random
import time
import numpy as np
import json
from os.path import dirname, join
def player2_handle_outcome(game_info):
    with open(join(dirname(__file__),'games_played'), 'a+') as f:
        f.write(json.dumps(game_info))
        f.write(f"\n {''.join(['=' for _ in range(100)])}\n")
def get_state_cards(cards):
    cards = cards['cards']
    if len(cards) == 0:
        return ''
    return ' | '.join(cards)
def playin_with_yourself(gamestate, player=''):

    """Play put the algorithm in here.  Input will be the gamestate formated
        {
        player_info:{}
        betting_info:{}
        betting_info.betting_options[]
        }
        if the choice in not in the betting_info.betting_options list will auto fold hand.

    return dictionary with {'choice': your choice, 'amount':bet amount}
    amount is only required when choice=bet
    """
    space = ''.join(['\n' for _ in range(5)])
    print(f"{10 * space}DECISION {player}")
    player_info = gamestate['player_info']
    betting_info = gamestate['betting_info']
    flop = player_info['flop']
    turn = player_info['turn']
    river = player_info['river']
    player_cards = player_info['hand']
    state_strings = zip(('player_cards flop turn river'.split()),
                        [get_state_cards(x) for x in (player_cards, flop, turn, river)])
    for state, string in state_strings:
        if len(string) > 0:
            print(f'{state}: {string}')
    to_call = betting_info['to_call']
    prev_choice = betting_info['previous_choice']
    player_banks = betting_info['player_banks']
    for x in player_banks:
        print(f'{x} bank: {player_banks[x]}')
    print(f'to call: {to_call} previous choice: {prev_choice}')
    to_ret = input(f"what do you want to do, options: {' '.join(betting_info['betting_options'])}{space}")

    if 'bet' in to_ret:
        to_ret = to_ret.split()
        if len(to_ret) == 1:
            to_ret.append(50)
        return {'choice': to_ret[0], 'amount': int(to_ret[1])}
    return {'choice': to_ret}
    """"
    if gamestate['player_info']['state'] == 'turn':
        print(gamestate['player_info'])
        assert len(gamestate['player_info']['turn']['cards']) == 1
        assert len(gamestate['player_info']['river']['cards']) == 0
        assert len(gamestate['player_info']['flop']['cards']) == 3

    player_info = gamestate['player_info']
    hand_matrix = player_info['hand']['hand_matrix']
    colapse = np.matmul(np.transpose(hand_matrix), np.ones(4))
    if np.max(colapse) > 1 and 'bet' in gamestate['betting_info']['betting_options']:
        print(gamestate['betting_info']['betting_options'])
        return {'choice': 'bet', 'amount': 100}
    else:
        if 'call' in gamestate['betting_info']['betting_options']:
            return {'choice': 'call'}
    options = gamestate['betting_info']['betting_options']
    choice = {'choice':random.choice(options)}
    if choice['choice'] == 'bet':
        choice['amount']=25
    return choice"""