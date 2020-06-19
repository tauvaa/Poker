#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from tensorflow import keras

MODEL_NAME = 'saved_model'
model = keras.models.load_model(join(dirname(__file__), MODEL_NAME))


def player_handle_outcome(gamestate):
    return


def playerchoice(gamestate):
    prediction = model.predict(gamestate)
    if 'check' not in gamestate['betting_info']['betting_options']:
        if (prediction.max() > 0.75):
            return {'choice': 'bet', 'amount': 25}
        return {'choice': 'call'}
    return {'choice': 'check'}
