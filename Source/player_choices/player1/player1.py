#!/usr/bin/env python3
import random
import numpy as np
import json
from os.path import join, dirname
def player1_handle_outcome(game_info):

    with open(join(dirname(__file__),'games_played'), 'a+') as f:
        f.write(json.dumps(game_info))
        f.write(f"\n {''.join(['=' for _ in range(100)])}\n")


def player1choice(gamestate):
    # print(f"player 1 bank: {gamestate['player_info']['bank']}")
    player_info = gamestate['player_info']
    # print(gamestate)
    # print(player_info['hand'].keys())
    # exit()
    hand_matrix = player_info['hand']['hand_matrix']
    if np.max(np.matmul(hand_matrix, np.ones(13))) >1 and 'bet' in gamestate['betting_info']['betting_options']:
        return {'choice': 'bet', 'amount': 25}
    else:
        if 'call' in gamestate['betting_info']['betting_options']:
            return {'choice': 'call'}
    options = gamestate['betting_info']['betting_options']
    choice = {'choice': random.choice(options)}
    if choice['choice'] == 'bet':
        choice['amount']=25
    return choice