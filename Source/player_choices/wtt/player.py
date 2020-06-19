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
import Source.player_choices.wtt.models.william.player as william_player


def player1_handle_outcome(gamestate):
    return


def player1choice(gamestate):
    # tolo_player.playerchoice(gamestate)
    # tyson_player.playerchoice(gamestate)
    # william_player.playerchoice(gamesate)
    return {'choice': 'check'}
