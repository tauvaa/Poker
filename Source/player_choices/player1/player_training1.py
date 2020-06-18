#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import  listdir

import Source.player_choices.player1.training1 as t

def player1_handle_outcome(game_info):
  return

def player1choice(gamestate):
    prediction = t.predict(gamestate)
    if 'check' not in gamestate['betting_info']['betting_options']:
        if (prediction.max() > 0.50):
            return {'choice': 'bet', 'amount':25}
        return {'choice': 'call'}
    return {'choice': 'check'}