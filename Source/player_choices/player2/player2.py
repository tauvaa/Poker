#!/user/bin/env python3
import random
import time
import numpy as np
import json
from os.path import dirname, join
from Source.player_choices.examples.player_input import random_choice, check_through

import Source.player_choices.wtt.models.tolo.player1 as tolo_player
import Source.player_choices.wtt.models.william.player as william_player


def player2_handle_outcome(game_info):
    return
    with open(join(dirname(__file__), 'games_played'), 'a+') as f:
        com_cards = game_info['community_cards']
        player_cards = game_info['player_cards']
        del game_info['player_cards']
        del game_info['community_cards']
        # print(com_cards)
        # print(player_cards)
        f.write(json.dumps(game_info))
        f.write(f"\n {''.join(['=' for _ in range(100)])}\n")


def get_state_cards(cards):
    cards = cards['cards']
    if len(cards) == 0:
        return ''
    return ' | '.join(cards)


def player2choice(gamestate):
    return william_player.playerchoice(gamestate)
    """Play put the algorithm in here.  Input will be the gamestate formated
        {
        player_info:{}
        betting_info:{}
        betting_info.betting_options[]
        }
        if the choice in not in the betting_info.betting_options list will auto fold hand.

    return dictionary with {'choice': your choice, 'amount':bet amount}
    amount is only required when choice=bet
    """
    return check_through(gamestate)
