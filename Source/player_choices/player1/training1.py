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

def get_bet(bet):
    return [
      #  [
            1 if bet['choice'] == 'call' else 0,
            1 if bet['choice'] == 'check' else 0,
            1 if bet['choice'] == 'bet' else 0,
            1 if bet['choice'] == 'fold' else 0,
  #      ],
#        bet.get('amount', 0)
    ]

def train_model():
    all_data = []
    x_list = []
    y_train = []

    for x in listdir(join(dirname(__file__), 'data_store')):
        to_ap = join(dirname(__file__), 'data_store', x)
        with open(to_ap, 'rb') as f:
            all_data.append(pickle.load(f))
    for k in all_data: 
        flop = np.array(k['community_cards']['flop']['hand_matrix']).flatten()
        turn = np.array(k['community_cards']['turn']['hand_matrix']).flatten()
        river = np.array(k['community_cards']['river']['hand_matrix']).flatten()
        player_end = np.array(
            k['player_cards']['player 1']['hand_matrix'] if k['is_fold'] else k['player_cards'][0]['player 1']['hand_matrix'],
            dtype=bool
        ).flatten()
        player_turn = np.logical_xor(player_end, river)
        player_flop = np.logical_xor(player_turn, turn)
        player_pre_flop = np.logical_xor(player_flop, flop)

        x_list.extend([player_end, player_turn, player_flop, player_pre_flop])
        y_train.extend(repeat(1 if k['winner'] == 'player 1' else 0, 4))

    x_train = np.array(x_list)
    # define the keras model
    model = Sequential()
    model.add(Dense(25, input_dim=52, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #fit it to the dataset
    model.fit(x_train, y_train, epochs=150, batch_size=10)
    #evaluate
    _, accuracy = model.evaluate(x_train, y_train)
    print('Accuracy: %.2f' % (accuracy*100))

    model.save(join(dirname(__file__), 'training1_model'))

def predict(gamestate):
    model = keras.models.load_model(join(dirname(__file__), 'training1_model'))
    hand = np.array(
        gamestate['player_info']['hand']['hand_matrix']
        ,dtype=bool
    ).flatten()
    return model.predict(np.array([hand]))

if __name__ == '__main__':
    train_model()