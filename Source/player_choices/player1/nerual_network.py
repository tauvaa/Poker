#!/usr/bin/env python3

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim
from os import listdir
from os.path import dirname, join
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.l1 = nn.Linear(17, 10)
        self.l2 = nn.Linear(10, 4)
        self.l3 = nn.Linear(4,1)
        # self.conv1 = nn.Conv2d(1, 6, 3)
        # self.conv2 = nn.Conv2d(6, 16, 3)
        # # an affine operation: y = Wx + b
        # self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        # self.fc2 = nn.Linear(120, 84)
        # self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = torch.sigmoid(self.l1(x))
        x = torch.sigmoid(self.l2(x))
        x = torch.sigmoid(self.l3(x))
        # x = [round(k) for k in x]
        # x = torch.tensor(x)
        # Max pooling over a (2, 2) window
        # x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        # x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        # x = x.view(-1, self.num_flat_features(x))
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = self.fc3(x)
        return x
def setup_nn(input, target, **kwargs):
    if 'save' in kwargs and kwargs['save']:
        if 'save_file' not in kwargs:
            raise RuntimeError("did not provide a save file")
        save_file = kwargs['save_file']
        save = kwargs['save']
        saved_files = [int(x.split('_')[-1]) for x in listdir(join(dirname(__file__), 'trained_models')) if x.startswith(save_file)]
        prefix = 0
        if len(saved_files) > 0:
            prefix = max(saved_files) + 1

        save_file = join(dirname(__file__), 'trained_models',f'{save_file}_{prefix}')
    else:
        save = False


    input = torch.from_numpy(input).float()
    print(input)
    target = torch.tensor(target).float()
    net = Net()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    counter = 0
    while True:
        out = net(input)
        if counter > 750000:
            if save:
                torch.save(net, save_file)
            return net
        counter += 1
        crit = nn.BCELoss()
        loss = crit(out, target).float()
        # if loss < 0.4:
        #     return out
        if counter % 100 == 0:
            print(counter)
            print(loss)

        net.zero_grad()
        loss.backward()
        optimizer.step()