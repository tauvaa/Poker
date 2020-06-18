#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from Source.player_choices.examples.player_input import playin_with_yourself, random_choice, check_pairs, check_through

def open_load_append(file_name, new_object):
    base_loc = join(dirname(__file__),'data_store','outcome_data')

    if file_name in listdir(join(dirname(__file__), 'data_store','outcome_data')):
        with open(join(base_loc, file_name), 'rb+') as f:
            to_app = pickle.load(f)
        to_app.append(new_object)
    else:
        to_app = [new_object]
    with open(join(base_loc, file_name), 'wb+') as f:
        f.write(pickle.dumps(to_app))

def player1_handle_outcome(game_info):
    # print(game_info)
    com_cards = game_info['community_cards']
    player_cards = game_info['player_cards']
    # del game_info['player_cards']
    # del game_info['community_cards']
    print(com_cards)
    print(player_cards)
    # open_load_append('test', game_info)
    next_data_file = listdir(join(dirname(__file__), 'data_store', 'outcome_data'))
    next_data_file = [x for x in next_data_file if x not in('outcome_data', 'state_data','test')]
    if len(next_data_file) == 0:
        next_data_file = 0
    else:
        next_data_file = [int(n) for n in next_data_file]
        next_data_file = max(next_data_file) + 1
    with open(join(dirname(__file__),'data_store/outcome_data',str(next_data_file) ), 'ab+') as f:
        f.write(pickle.dumps(game_info))
        # f.write()
        # f.write(f"\n {''.join(['=' for _ in range(100)])}\n")


def player1choice(gamestate):
    # print(gamestate['betting_info']['min_bet'])
    # next_data_file = listdir(join(dirname(__file__), 'state_data'))
    # if len(next_data_file) == 0:
    #     next_data_file = 0
    # else:
    #     next_data_file = [int(n) for n in next_data_file]
    #     next_data_file = max(next_data_file) + 1

    # open_load_append('test', gamestate)
    # with open(join(dirname(__file__),'data_store/state_date',str(next_data_file) ), 'ab+') as f:
    #     f.write(pickle.dumps(gamestate))
    return check_through(gamestate)
