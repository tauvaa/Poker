#!/usr/bin/env python3
import random
import numpy as np
def player1choice(gamestate):
    # print(f"player 1 bank: {gamestate['player_info']['bank']}")
    player_info = gamestate['player_info']
    # print(gamestate)
    # print(player_info['hand'].keys())
    # exit()
    hand_matrix = player_info['hand']['hand_matrix']
    if np.max(np.matmul(hand_matrix, np.ones(13))) >1:
        return {'choice': 'bet', 'amount': 25}
    else:
        return {'choice': 'call'}
    options = gamestate['betting_info']['betting_options']
    choice = {'choice': random.choice(options)}
    if choice['choice'] == 'bet':
        choice['amount']=25
    return choice