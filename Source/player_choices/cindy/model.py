#!/usr/bin/env python3

import pickle
import numpy as np
from itertools import repeat
import datetime

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import TensorBoard
import joblib
from sklearn.model_selection import train_test_split

from os import listdir
from os.path import dirname, join, exists
import pprint

MODEL_NAME = 'model.pkl'


def init():
    # define the keras model
    model = Sequential()
    model.add(Dense(32, input_dim=52, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    save(model)
    return model


def save(model):
    joblib.dump(model, join(dirname(__file__), MODEL_NAME))


def load():
    model_file = join(dirname(__file__), MODEL_NAME)
    if exists(model_file):
        model = joblib.load(join(dirname(__file__), MODEL_NAME))
    else:
        model = init()
    model.summary()
    return model


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
    log_dir = join(dirname(__file__), "logs/")
    tensor_log = log_dir + "fit/{}" + datetime.datetime.now().strftime(
        "%Y%m%d-%H%M%S")
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
    #fit it to the dataset
    x_train, x_val, y_train, y_val = train_test_split(x_train,
                                                      y_train,
                                                      test_size=0.20,
                                                      shuffle=True)

    history = model.fit(
        x_train,
        y_train,
        epochs=50,
        batch_size=32,
        validation_data=(x_val, y_val),
        callbacks=[tensorboard_callback],
    )
    #evaluate
    loss, accuracy = model.evaluate(x_train, y_train)
    with open(log_dir + 'log.txt', "a") as log:
        log.write('Accuracy: %.2f' % (accuracy * 100) + ', Loss: %.2f' %
                  (loss * 100) + '\n')
        log.write(str(history.history))
        log.write('\n--------------------\n')
    save(model)


def predict(model, gamestate):
    hand = np.array(gamestate['player_info']['hand']['hand_matrix'],
                    dtype=bool).flatten()
    return model.predict(np.array([hand]))