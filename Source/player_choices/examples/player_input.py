#!/user/bin/env python3
import random
import time
import numpy as np
import json
from os.path import dirname, join

def generic_handle_outcome(game_info):
    print(game_info)
    # with open(join(dirname(__file__),'games_played'), 'a+') as f:
        # f.write(json.dumps(game_info))
        # f.write(f"\n {''.join(['=' for _ in range(100)])}\n")
def get_state_cards(cards):
    cards = cards['cards']
    if len(cards) == 0:
        return ''
    return ' | '.join(cards)

def check_pairs(gamestate):
    player_hand = gamestate['player_info']['hand']['hand_matrix']
    compress = np.matmul(np.transpose(player_hand), np.ones(4))
    print(compress)
    if compress.max()>1 or sum(compress[10:])>1:
        if 'bet' in gamestate['betting_info']['betting_options']:

            return {'choice': 'bet', 'amount':50}

        elif 'call' in gamestate['betting_info']['betting_options']:
            print(f'here are the betting options: {gamestate["betting_info"]["betting_options"]}')
            return {'choice': 'call'}
        else:
            return {'choice': 'check'}
    else:
        return {'choice':'fold'}

def setup(gamestate,player=''):
    space = ''.join(['\n' for _ in range(5)])
    print(f"{space}DECISION {player}")
    player_info = gamestate['player_info']
    betting_info = gamestate['betting_info']
    flop = player_info['flop']
    turn = player_info['turn']
    river = player_info['river']
    player_cards = player_info['hand']
    state_strings = zip(('player_cards flop turn river'.split()),
                        [get_state_cards(x) for x in (player_cards, flop, turn, river)])
    board_string = ''
    for state, string in state_strings:
        if len(string) > 0:
            board_string += f'| {string}'
    if len(board_string)>0:
        print(f'board: {board_string}')
    to_call = betting_info['to_call']
    prev_choice = betting_info['previous_choice']
    player_banks = betting_info['player_banks']
    for x in player_banks:
        print(f'{x} bank: {player_banks[x]}')
    print(f'previous choice: {prev_choice}')
    print(f'to call: {to_call}')

def random_choice(gamestate, player=''):
    setup(gamestate, player)
    betting_options = gamestate['betting_info']['betting_options']
    option = random.choice(betting_options)
    with open('player_options', 'a+') as f:
        f.write(f'{option}\n')
    print(f'{option}!!!!!!!!!!!!!!!!!!!!!!')
    if option == 'bet':
        return {'choice':option,'amount':25}
    if option == 'call':
        return {'choice': 'call'}
    if option == 'check' or (option=='fold' and 'check' in betting_options):
        return {'choice': 'check'}
    # time.sleep(1)
    return {'choice': option}

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
    setup(gamestate, player='player 1')
    player_info = gamestate['player_info']
    betting_info = gamestate['betting_info']

    to_ret = input(f"what do you want to do, options: {' '.join(betting_info['betting_options'])}\n")

    if 'bet' in to_ret:
        to_ret = to_ret.split()
        if len(to_ret) == 1:
            to_ret.append(50)
        return {'choice': to_ret[0], 'amount': int(to_ret[1])}
    return {'choice': to_ret}