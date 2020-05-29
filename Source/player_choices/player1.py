#!/usr/bin/env python3
import random
def player1choice(gamestate):
    # print(f"player 1 bank: {gamestate['player_info']['bank']}")
    options = gamestate['betting_info']['betting_options']
    choice = {'choice': random.choice(options)}
    if choice['choice'] == 'bet':
        choice['amount']=10
    return choice