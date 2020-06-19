#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from Source.player_choices.examples.player_input import check_through
import Source.player_choices.wtt.models.tyson.model as tyson_model

model = tyson_model.load()
realtime_data = []

TRAINING = False
HANDS_PLAYED_BATCH_SIZE = 10000
REALTIME = False


def train(gamestate):
    if len(realtime_data) < HANDS_PLAYED_BATCH_SIZE * 4:
        realtime_data.append(gamestate)
    else:
        [x_train, y_train] = tyson_model.parse_data(realtime_data)
        tyson_model.train(model, x_train, y_train)
        realtime_data.clear()


def player_handle_outcome(gamestate):
    if TRAINING:
        train(gamestate) if REALTIME else tyson_model.save_data(gamestate)
    return


def choose(gamestate):
    prediction = tyson_model.predict(model, gamestate)
    if 'check' not in gamestate['betting_info']['betting_options']:
        if (prediction.max() > 0.75):
            return {'choice': 'bet', 'amount': 25}
        return {'choice': 'call'}
    return {'choice': 'check'}


def playerchoice(gamestate):
    return check_through(gamestate) if TRAINING else choose(gamestate)
