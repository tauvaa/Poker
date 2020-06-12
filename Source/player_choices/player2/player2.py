#!/user/bin/env python3
import random
import time
import numpy as np
def player2choice(gamestate):

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
    return choice