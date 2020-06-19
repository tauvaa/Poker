#!/usr/bin/env python3

import pickle

from os import listdir
from os.path import dirname, join
import pprint
import numpy as np
from Source.player_choices.player1.nerual_network import setup_nn
from torch import Tensor
import torch
class TrainUnit:
    flatten = True
    def __init__(self,hand_matrix, community_cards, outcome):
        x = np.zeros(shape=(4,13))
        for j in community_cards:
            x += j
        self.hole_matrix = hand_matrix - x
        self.hand_matrix = hand_matrix
        self.community_cards = community_cards
        self._hole_array()
        self._flop_array()
        self._turn_array()
        self._river_array()
        self.outcome = outcome


    def add_community_cards(self, mat):
        self.community_cards.append(mat)

    def make_array(self, mat):
        if not self.flatten:
            pairs = self.get_pairs(mat)
            suits = self.get_suits(mat)
            return np.transpose(np.row_stack((pairs, suits)))[0]
        return mat.flatten()


    def get_suits(self, mat):
        # print(mat)
        return np.matmul(mat, np.ones((13,1)))

    def get_pairs(self, mat):
        # print(mat)
        return np.matmul(np.transpose(mat), np.ones((4,1)))
    def _hole_array(self):
        self.hole_array = self.make_array(self.hole_matrix)

    def _flop_array(self, ):
        self.flop_array = self.make_array(self.community_cards[0] + self.hole_matrix)

    def _turn_array(self):
        self.turn_array = self.make_array(self.community_cards[1] + self.hole_matrix + self.community_cards[0])
    def _river_array(self):
        self.river_array = self.make_array(self.community_cards[2] + self.hole_matrix + self.community_cards[0] + self.community_cards[1])

def get_data():
    with open('data_store/outcome_data/test', 'rb') as f:
        # for _ in f:
        all_data = pickle.load(f)
        X = []
        for row in all_data:
            # print(row)
            hand_matrix = row['player_cards'][0]['player 1']['hand_matrix']
            flop, turn, river = (row['community_cards'][x]['hand_matrix'] for x in ('flop', 'turn', 'river'))
            outcome = row['winner']
            if outcome == 'player 1':
                outcome = 1
            else:
                outcome = 0
            tu = TrainUnit(hand_matrix, community_cards=[flop, turn, river], outcome=outcome)
            X.append(tu)
    return X


def transform_data(element):
    hand_matrix = element['player_cards'][0]['player 1']['hand_matrix']
    flop, turn, river = (element['community_cards'][x]['hand_matrix'] for x in ('flop', 'turn', 'river'))
    outcome = element['winner']
    if outcome == 'player 1':
        outcome = 1
    else:
        outcome = 0
    tu = TrainUnit(hand_matrix, community_cards=[flop, turn, river], outcome=outcome)
    return tu



def condense_data(number_units=10000, run_all=False):
    all_data = []
    count = 0
    for file in listdir(join(dirname(__file__), 'data_store', 'outcome_data')):
        if count > number_units:
            break
        if file != 'test' and file != '00clean_up.py':
            with open(join(dirname(__file__), 'data_store', 'outcome_data', file), 'r+b') as f:
                data = pickle.load(f)
                all_data.append(transform_data(data))
        if not run_all:
            count += 1
    return all_data

def train_model(state, batch_size):
    data = condense_data(50000)
    if state == 'flop':
        data = ([x.outcome, x.flop_array] for x in data)
    elif state == 'turn':
        data = ([x.outcome, x.turn_array] for x in data)
    elif state == 'river':
        data = ([x.outcome, x.river_array] for x in data)
    elif state == 'preflop':
        data = ([x.outcome, x.hole_array] for x in data)

    X, Y = [], []
    for x in data:
        Y.append(x[0])
        X.append(x[1])

    X = np.row_stack(X)
    Y = np.array(Y)
    mask = np.random.rand(len(Y))>0.2
    X_train, Y_train = X[mask], Y[mask]
    X_test, Y_test = X[~mask], Y[~mask]
    position = 0
    training_batches = []
    while len(Y_train) - position >= batch_size:
        training_batches.append([X_train[position: position+batch_size], Y_train[position: position+batch_size]])
        position += batch_size
    # print(training_batches)
    if TrainUnit.flatten:
        sf = f'{state}-flatten'
    else:
        sf=state
    modl = setup_nn(training_batches, save=True, save_file=sf,epochs=8)
    output = modl(torch.from_numpy(X_test).float())
    return Y_test, output
def train_test():
    for x in 'preflop flop turn river'.split():
        target, predict = train_model(x, batch_size=100)
        predict = predict.detach().numpy()
    # predict = np.array([1 if y > 0.5 else 0 for y in predict])
        predict = np.array([x[0] for x in predict])
        print(predict)
        diff = predict - target
        print(sum(diff))
if __name__ == '__main__':
    # d = condense_data(10)
    # print(d[0].turn_array)
    train_test()

    # X = get_data()
    # print(len(X))

    # print(np.dot(diff, diff)/len(diff))
    # print(diff)
    # print(output)
    # train_model()
            # print(x)
        # print(outcome)
        # print(x)
        # print(x[4])
        # print(pickle.load(f))
        # for line in f:
        #     print(pickle.loads(line))
