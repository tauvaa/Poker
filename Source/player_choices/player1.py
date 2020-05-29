#!/usr/bin/env python3
import random
def player1choice(gamestate):
    options = gamestate['betting_info']['betting_options']
    choice = {'choice': random.choice(options)}
    if choice == 'bet':
        choice['amount']=500
    return {'choice':'check', 'amount':500}