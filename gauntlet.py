#!/usr/bin/env python3


import os
import json
from os.path import dirname, join
from main import play_games
# koth_path = join(dirname(__file__), 'Source', 'player_choices','player1','king_of_the_hill')
chal_path = join(dirname(__file__), 'Source', 'player_choices','wtt','models','tolo', 'challenge')
def get_prefix():
    all_models = os.listdir(join(dirname(__file__), 'Source', 'player_choices','wtt','models','tolo','trained_models'))
    to_ret = []
    f = lambda sep, x: sep+x.split(sep)[-1]
    for x in all_models:
        if '-' in x:
            to_app = f('-',x)

        else:
            to_app = f('_', x)
        if to_app not in to_ret:
            to_ret.append(to_app)

    return to_ret


if __name__ == '__main__':
    ALL_MODELS = get_prefix()


    for CHALLENGER in  ALL_MODELS:
        with open(chal_path, 'w') as f:
            f.write(CHALLENGER)
        counter = play_games(5)
        x = counter['player 1'] > counter['player 2']

        if x:
            winner_count = counter['player 1']
            loser_count = counter['player 2']
            winner = CHALLENGER
        else:
            winner_count = counter['player 2']
            loser_count = counter['player 1']
            winner = 'player 2'

        with open('matchups', 'a+') as f:

            f.write(json.dumps(dict(
                                    challenger=CHALLENGER,
                                    winner=winner,
                                    winner_count=winner_count,
                                    loser_count=loser_count,
                                    counter=counter)) + '\n')
            # f.write('\n')
