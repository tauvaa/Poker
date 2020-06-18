#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from Source.player_choices.examples.player_input import playin_with_yourself, random_choice, check_pairs, check_through
import Source.player_choices.cindy.model as cindy_model


def player1_handle_outcome(game_info):
    #realtime_training(game_info)
    return


def player1choice(gamestate):
    # print(gamestate['betting_info']['min_bet'])
    return check_through(gamestate)