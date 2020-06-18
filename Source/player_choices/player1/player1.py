#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from Source.player_choices.examples.player_input import playin_with_yourself, random_choice, check_pairs, check_through


def player1_handle_outcome(game_info):
    # print(game_info)
    com_cards = game_info['community_cards']
    player_cards = game_info['player_cards']
    # del game_info['player_cards']
    # del game_info['community_cards']
    print(com_cards)
    print(player_cards)

    next_data_file = listdir(join(dirname(__file__), 'data_store'))
    if len(next_data_file) == 0:
        next_data_file = 0
    else:
        next_data_file = [int(n) for n in next_data_file]
        next_data_file = max(next_data_file) + 1
    with open(join(dirname(__file__), 'data_store', str(next_data_file)),
              'ab+') as f:
        f.write(pickle.dumps(game_info))
        # f.write(f"\n {''.join(['=' for _ in range(100)])}\n")


def player1choice(gamestate):
    # print(gamestate['betting_info']['min_bet'])
    return check_through(gamestate)