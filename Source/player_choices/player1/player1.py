#!/usr/bin/env python3
import random
import numpy as np
import json
from os.path import join, dirname
from Source.player_choices.examples.player_input import playin_with_yourself, random_choice, check_pairs, check_through
def player1_handle_outcome(game_info):
    # print(game_info)
    com_cards = game_info['community_cards']
    player_cards = game_info['player_cards']
    del game_info['player_cards']
    del game_info['community_cards']
    # print(com_cards)
    # print(player_cards)
    with open(join(dirname(__file__),'games_played'), 'a+') as f:
        f.write(json.dumps(game_info))
        f.write(f"\n {''.join(['=' for _ in range(100)])}\n")


def player1choice(gamestate):
    print(gamestate['betting_info']['min_bet'])
    return random_choice(gamestate)
