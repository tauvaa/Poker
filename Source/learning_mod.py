#!/usr/bin/python3

import numpy as np

class training_element:
    def __init__(self):
        self.Hand = None
        self.Flop = None
        self.Turn = None
        self.River = None
        self.Outcome = None
    
    def add_hand(self,card1,card2):
        self.Hand = np.array([card1,card2])
        self.Hand=np.transpose(self.Hand)
        self.Hand = self.Hand[:,0]+self.Hand[:,1]
    
    def add_flop(self,card1,card2,card3):
        self.Flop=np.array([card1,card2,card3])
        self.Flop = np.transpose(self.Flop)
        temp = np.zeros(len(self.Flop[:,0]))
        for i in range(3):
            temp+=self.Flop[:,i]
        self.Flop = temp
        
    def add_turn(self, card1):
        self.Turn = np.array(card1)
    
    def add_river(self,card1):
        self.River = np.array(card1)
    
    def create_training_element(self,card):
        def map_suit(card):
            if card.suit =='Club':
                return 0
            elif card.suit=='Diamond':
                return 1
            elif card.suit=='Heart':
                return 2
            elif card.suit=='Spade':
                return 3
        to_ret = np.zeros(17)
        to_ret[card.value-1]=1
        to_ret[13+map_suit(card)]=1
        return to_ret
    
    def print_element(self):
        print("Hand")
        print(self.Hand)
        print("Flop")
        print(self.Flop)
        print("Turn")
        print(self.Turn)
        print("River")
        print(self.River)
        print("Outcome")
        print(self.Outcome)

    
import statsmodels.discrete.discrete_model as sm
def model_training(training_set,level):
    """model training method, will take in a training set and
    return a trained model"""
    x_values = []
    y_values = []
    for element in training_set:
        y_values.append(element.Outcome)
        if level == 'Hand':
            x_values.append(element.Hand)
        elif level == 'Flop':
            x_values.append(element.Hand+element.Flop)
        elif level == 'Turn':
            x_values.append(element.Hand+element.Flop+element.Turn)
        elif level == 'River':
            x_values.append(element.Hand+element.Flop+element.Turn+element.River)
    #print(y_values)
    #pprint(x_values)
    model = sm.Logit(np.array(y_values),np.array(x_values))
    return model.fit()

def model_testing(test_set,model,level):
    to_ret = []
    for i in range(len(test_set)):
        element = test_set[i]
        outcome = element.Outcome
        if level == 'Hand':
            x_value=element.Hand
        elif level == 'Flop':
            x_value=element.Hand+element.Flop
        elif level == 'Turn':
            x_value=element.Hand+element.Flop+element.Turn
        elif level == 'River':
            x_value=element.Hand+element.Flop+element.Turn+element.River
        y_pred = model.predict(x_value)
        if y_pred>0.5:
            y_pred=1
        elif y_pred<0.5:
            y_pred = 0
        else:
            y_pred = 0.5
            
        if y_pred-outcome!=0:
            to_ret.append(1)
        else:
            to_ret.append(0)
        #to_ret.append(abs(y_pred - outcome))
    return to_ret
        
    


