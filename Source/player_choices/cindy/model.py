#!/usr/bin/env python3

import pickle
import numpy as np
from itertools import repeat

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense

from os import listdir
from os.path import dirname, join
import pprint

MODEL_NAME = 'model'


def init():
    # define the keras model
    model = Sequential()
    model.add(Dense(32, input_dim=52, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()
    # compile model
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    save(model)
    # save
    return model


def save(model):
    model.save(join(dirname(__file__), MODEL_NAME))


def load():
    return keras.models.load_model(join(dirname(__file__), MODEL_NAME))


def save_data(game_info):
    next_data_file = listdir(join(dirname(__file__), 'data_store'))
    if len(next_data_file) == 0:
        next_data_file = 0
    else:
        next_data_file = [int(n) for n in next_data_file]
        next_data_file = max(next_data_file) + 1
    with open(join(dirname(__file__), 'data_store', str(next_data_file)),
              'ab+') as f:
        f.write(pickle.dumps(game_info))


def load_data():
    all_data = []
    for x in listdir(join(dirname(__file__), 'data_store')):
        to_ap = join(dirname(__file__), 'data_store', x)
        with open(to_ap, 'rb') as f:
            all_data.append(pickle.load(f))
    return all_data


def parse_data(game_info_array):
    x_list = []
    y_train = []
    for k in game_info_array:
        flop = np.array(k['community_cards']['flop']['hand_matrix']).flatten()
        turn = np.array(k['community_cards']['turn']['hand_matrix']).flatten()
        river = np.array(
            k['community_cards']['river']['hand_matrix']).flatten()
        player_end = np.array(
            k['player_cards']['player 1']['hand_matrix'] if k['is_fold'] else
            k['player_cards'][0]['player 1']['hand_matrix'],
            dtype=bool).flatten()
        player_turn = np.logical_xor(player_end, river)
        player_flop = np.logical_xor(player_turn, turn)
        player_pre_flop = np.logical_xor(player_flop, flop)

        x_list.extend([player_end, player_turn, player_flop, player_pre_flop])
        y_train.extend(repeat(1 if k['winner'] == 'player 1' else 0, 4))
    return [np.array(x_list), y_train]


def train(model, x_train, y_train):
    #fit it to the dataset
    model.fit(x_train, y_train, epochs=150, batch_size=32)
    #evaluate
    _, accuracy = model.evaluate(x_train, y_train)
    print('Accuracy: %.2f' % (accuracy * 100))
    model.save(join(dirname(__file__), 'training_check_through_model'))


def predict(model, gamestate):
    hand = np.array(gamestate['player_info']['hand']['hand_matrix'],
                    dtype=bool).flatten()
    return model.predict(np.array([hand]))