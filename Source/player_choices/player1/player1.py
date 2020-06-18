#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
import Source.player_choices.cindy.player as cindy_player


def player1_handle_outcome(game_info):
    return cindy_player.player1_handle_outcome(game_info)


def player1choice(gamestate):
    return cindy_player.player1choice(gamestate)