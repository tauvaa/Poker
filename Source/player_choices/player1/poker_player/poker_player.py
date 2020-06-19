#!/usr/bin/env python3
import os
from os.path import dirname, join, split
import torch
import numpy as np

class PokerPlayer:

    def __init__(self, trained_models, state, hand_matrix, flatten):
        for k in 'preflop flop turn river'.split():
            trained_models[k] = join(split(dirname(__file__))[0],'trained_models', trained_models[k])
        def f(n): return torch.load(trained_models[n])
        self.model = f(state)
        self.flatten = flatten
        # self.preflop_model = f('preflop')

        # self.flop_model = f('flop')
        # self.turn_model = f('turn')
        # self.river_model = f('river')
        self.state = state
        self.hand_matrix = hand_matrix

    def apply_model(self, data):
        if not self.flatten:
            pairs = np.matmul(data, np.ones((13, 1)))
            suits = np.matmul(np.transpose(data), np.ones((4, 1)))
            data = np.transpose(np.row_stack((pairs, suits)))[0]
            return self.model(torch.from_numpy(data).float())
        else:
            return self.model(torch.from_numpy(data.flatten()).float())