#!/usr/bin/env python3
import random
import numpy as np
import json
import pprint
import pickle
from os.path import join, dirname
from os import listdir
from Source.player_choices.examples.player_input import playin_with_yourself, random_choice, check_pairs, check_through
from .poker_player.poker_player import PokerPlayer
from .training import TrainUnit
with open(join(dirname(__file__), 'king_of_the_hill'), 'r') as f:
    KING=f.read()
with open('bid_coff') as f:
    BID_COFF = int(f.read().strip())
def transform_data(gamestate):
    player_info = gamestate['player_info']
    hand = player_info['hand']['hand_matrix']

    f = lambda x: player_info[x]['matrix']
    for x in ('flop', 'turn', 'river'):
        hand += f(x)
    return hand


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

    # next_data_file = listdir(join(dirname(__file__), 'data_store', 'outcome_data'))
    # next_data_file = [x for x in next_data_file if x not in('outcome_data', 'state_data','test')]
    # if len(next_data_file) == 0:
    #     next_data_file = 0
    # else:
    #     next_data_file = [int(n) for n in next_data_file]
    #     next_data_file = max(next_data_file) + 1
    # with open(join(dirname(__file__),'data_store/outcome_data',str(next_data_file)), 'ab+') as f:
    #     f.write(pickle.dumps(game_info))

        # f.write()
        # f.write(f"\n {''.join(['=' for _ in range(100)])}\n")



    prefix = 'game_outcomes-9'
    save_files = [int(x.split('_')[-1]) for x in listdir(join(dirname(__file__), 'data_store', 'state_data')) if x.startswith(prefix)]
    # print(game_info)
    postfix = max(save_files)
    file_name = f'{prefix}_{postfix}'
    with open(join(dirname(__file__),'data_store', 'state_data', file_name)) as f:
        dic = json.load(f)
        dic['outcome'] = game_info['winner']
        dic['player1_hand'] = ' | '.join([x.card_string() for x in game_info['player_cards'][0]['player 1']['cards']])
        dic['player2_hand'] = ' | '.join([x.card_string() for x in game_info['player_cards'][1]['player 2']['cards']])

    with open(join(dirname(__file__),'data_store', 'state_data', file_name), 'w') as f:
        f.write(json.dumps(dic))

def model_reader(gamestate, fn_name):
    with open(join(dirname(__file__), fn_name)) as f:
        prefix = f.read()
    model_paths = {x:x+prefix for x in 'preflop flop turn river'.split()}
    flatten = 'flatten' in prefix
    pp = PokerPlayer(model_paths, gamestate['player_info']['state'], transform_data(gamestate), flatten=flatten)
    perc = pp.apply_model(transform_data(gamestate))
    perce = perc.detach().numpy()[0]
    min_bet = max(25, int(gamestate['betting_info']['min_bet']))
    to_call = int(gamestate['betting_info']['to_call'])
    pot_worth = 1.25 * (1 / 0.4) * perce * min_bet - to_call
    betting_options = gamestate['betting_info']['betting_options']
    if pot_worth < 0 and 'check' not in betting_options:
        return {'choice': 'fold'}
    elif pot_worth < min_bet:

        if 'call' in betting_options:
            return {'choice': 'call'}
        else:
            return {'choice': 'check'}
    else:
        if 'bet' in betting_options:
            return {'choice': 'bet', 'amount': min_bet}
        elif 'call' in betting_options:
            return {'choice': 'call'}
        else:
            return {'choice': 'check'}


def model_user(gamestate, flatten=True):

    def f(x):
        if flatten:
            return 'flatten' in x
        else:
            return not 'flatten' in x


    model_number = max([int(x.split('_')[-1]) for x in listdir(join(dirname(__file__), 'trained_models')) if f(x)])
    if flatten:
        addon='-flatten'
    else:
        addon=''

    model_paths = {x: f'{x}{addon}_{model_number}' for x in 'flop turn river preflop'.split()}
    pp = PokerPlayer(model_paths, gamestate['player_info']['state'], transform_data(gamestate), flatten=flatten)
    perc = pp.apply_model(transform_data(gamestate))
    perce = perc.detach().numpy()[0]
    min_bet = max(50, int(gamestate['betting_info']['min_bet']))
    to_call = int(gamestate['betting_info']['to_call'])
    pot_worth = 1.25*(1/0.4)*perce*min_bet-to_call
    betting_options = gamestate['betting_info']['betting_options']
    if pot_worth < 0 and 'check' not in betting_options:
        return {'choice':'fold'}
    elif pot_worth < min_bet:

        if 'call' in betting_options:
            return {'choice':'call'}
        else:
            return {'choice':'check'}
    else:
        if 'bet' in betting_options:
            return {'choice': 'bet', 'amount':min_bet}
        elif 'call' in betting_options:
            return {'choice':'call'}
        else:
            return {'choice':'check'}


def run_model(gamestate, prefix):
    flatten = 'flatten' in prefix
    model_paths = {x: f'{x}{prefix}' for x in 'flop turn river preflop'.split()}
    pp = PokerPlayer(model_paths, gamestate['player_info']['state'], transform_data(gamestate), flatten=flatten)
    perc = pp.apply_model(transform_data(gamestate))
    perce = perc.detach().numpy()[0]
    min_bet = max(25, int(gamestate['betting_info']['min_bet']))
    to_call = int(gamestate['betting_info']['to_call'])
    pot_worth = BID_COFF*1.25 * (1 / 0.4) * perce * min_bet - to_call
    betting_options = gamestate['betting_info']['betting_options']
    if pot_worth < 0 and 'check' not in betting_options:
        return {'choice': 'fold'}
    elif pot_worth < min_bet:

        if 'call' in betting_options:
            return {'choice': 'call'}
        else:
            return {'choice': 'check'}
    else:
        if 'bet' in betting_options:
            return {'choice': 'bet', 'amount': min_bet}
        elif 'call' in betting_options:
            return {'choice': 'call'}
        else:
            return {'choice': 'check'}
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
    # return check_pairs(gamestate)
    # return model_user(gamestate)
    model_reader(gamestate, 'challenge')
    prefix = 'game_outcomes-6'
    save_files = [int(x.split('_')[-1]) for x in listdir(join(dirname(__file__),'data_store', 'state_data')) if x.startswith(prefix)]
    postfix = 0
    #
    model_paths = {x: f'{x}_6' for x in 'flop turn river preflop'.split()}
    # print(model_paths)
    pp = PokerPlayer(model_paths, gamestate['player_info']['state'], transform_data(gamestate), flatten=False)
    perc = pp.apply_model(transform_data(gamestate))
    if gamestate['player_info']['state'] == 'preflop':
        if len(save_files) > 0:
            postfix = max(save_files) + 1
    #
        with open(join(dirname(__file__), 'data_store','state_data', f'{prefix}_{postfix}'), 'w+') as f:
            f.write(json.dumps({}))
    else:
        postfix = max(save_files)
    file_name = f'{prefix}_{postfix}'
    with open(join(dirname(__file__),'data_store', 'state_data', file_name)) as f:
        dic = json.load(f)
        dic[gamestate['player_info']['state']] = float(perc.detach().numpy()[0])
    with open(join(dirname(__file__),'data_store' ,'state_data', file_name), 'w') as f:
        f.write(json.dumps(dic))

    # return check_through(gamestate)
    return run_model(gamestate, '_6')

    #return check_through(gamestate)
