#!/usr/bin/env python3

import pickle

from os import listdir
from os.path import dirname, join
import pprint
import numpy as np
from Source.player_choices.player1.nerual_network import setup_nn
from torch import Tensor
class TrainUnit:
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
        pairs = self.get_pairs(mat)
        suits = self.get_suits(mat)
        return np.transpose(np.row_stack((pairs, suits)))[0]

    def get_suits(self, mat):
        # print(mat)
        return np.matmul(mat, np.ones((13,1)))

    def get_pairs(self, mat):
        # print(mat)
        return np.matmul(np.transpose(mat), np.ones((4,1)))
    def _hole_array(self):

        self.hole_array = self.make_array(self.hole_matrix)
    def _flop_array(self):
        self.flop_array = self.make_array(self.community_cards[0])

    def _turn_array(self):
        self.turn_array = self.make_array(self.community_cards[1])
    def _river_array(self):
        self.turn_array = self.make_array(self.community_cards[2])

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
        if file != 'test':
            with open(join(dirname(__file__), 'data_store', 'outcome_data', file), 'r+b') as f:
                data = pickle.load(f)
                all_data.append(transform_data(data))
        if not run_all:
            count += 1
    return all_data

def train_model(state):
    data = condense_data(20000)
    if state == 'flop':
        data = ([x.outcome, x.flop_array] for x in data)
    X, Y = [], []
    for x in data:
        Y.append(x[0])
        X.append(x[1])

    X = np.row_stack(X)
    Y = np.array(Y)
    mask = np.random.rand(len(Y))>0.2
    X_train, Y_train = X[mask], Y[mask]
    X_test, Y_test = X[~mask], Y[~mask]


    modl = setup_nn(X_train, Y_train, save=True, save_file=state)
    output = modl(Tensor(X_test))
    return Y_test, output

if __name__ == '__main__':
    # X = get_data()
    # print(len(X))
    target, predict = train_model('flop')
    predict = predict.detach().numpy()
    predict = np.array([1 if y > 0.5 else 0 for y in predict])
    diff = predict - target
    print(np.dot(diff, diff)/len(diff))
    print(diff)
    # print(output)
    # train_model()
            # print(x)
        # print(outcome)
        # print(x)
        # print(x[4])
        # print(pickle.load(f))
        # for line in f:
        #     print(pickle.loads(line))
