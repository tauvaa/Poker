#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
import Source.player_choices.wtt.models.tyson.player as tyson_player
import Source.player_choices.wtt.models.tolo.player1 as tolo_player


def player1_handle_outcome(gamestate):
    return


def player1choice(gamestate):
    # tolo_player.player1choice(gamestate)
    # tyson_player.player1choice(gamestate)
    return {'choice': 'check'}
