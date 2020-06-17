#!/usr/bin/env python3

import pickle

from os import listdir
from os.path import dirname, join
import pprint

def train_model():
    all_data = []
    for x in listdir(join(dirname(__file__), 'data_store')):
        to_ap = join(dirname(__file__), 'data_store', x)
        with open(to_ap, 'rb') as f:
            all_data.append(pickle.load(f))
    for k in all_data: pprint.pprint(k)



if __name__ == '__main__':
    train_model()