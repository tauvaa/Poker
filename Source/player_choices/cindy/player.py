#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir

import Source.player_choices.cindy.model as cindy_model


def handle_outcome(game_info):
    return


def choose(gamestate):
    prediction = cindy_model.predict(gamestate)
    if 'check' not in gamestate['betting_info']['betting_options']:
        if (prediction.max() > 0.75):
            return {'choice': 'bet', 'amount': 25}
        return {'choice': 'call'}
    return {'choice': 'check'}