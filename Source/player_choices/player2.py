#!/user/bin/env python3
import random
import time
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
    player_info = gamestate['player_info']
    betting_info = gamestate['betting_info']
    for state in 'hand flop turn river'.split():
        x = player_info[state]['cards']
        if len(x) > 0:
            pass #print(f'state: {state}, cards: {x}')
    # print(player_info)
    # print(player_info['bank'])
    # time.sleep(.1)
    options = gamestate['betting_info']['betting_options']
    choice = {'choice':random.choice(options)}
    if choice == 'bet':
        choice['amount']=100
    return {'choice':'check'}