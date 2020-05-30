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

    # print(gamestate)
    player_info = gamestate['player_info']
    hand_matrix = player_info['hand']['hand_matrix']
    colapse = np.matmul(np.transpose(hand_matrix), np.ones(4))
    if np.max(colapse) > 1 and 'bet' in gamestate['betting_info']['betting_options']:
        print(gamestate['betting_info']['betting_options'])
        return {'choice': 'bet', 'amount': 100}
    else: return {'choice': 'call'}
    betting_info = gamestate['betting_info']

    # print(player_info)
    # print(player_info['bank'])
    # time.sleep(.1)
    options = gamestate['betting_info']['betting_options']
    choice = {'choice':random.choice(options)}
    if choice['choice'] == 'bet':
        choice['amount']=25
    # print(f"player 2 bank: {gamestate['player_info']['bank']}")
    return choice