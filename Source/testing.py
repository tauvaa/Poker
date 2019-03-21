#!/usr/bin/python3


"""This is the testing area for game applicaton"""

from Source.game import *
from Source.betting import *
from Source.learning_mod import *
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras


player1 = player('player1')
player2 = player('player2')

#b = betting(player1,player2,1)
#x=b.decide()
#f = open('game_log.txt','w')
def print_cards(cards):
    for c in cards:
        print(c.value,c.suit)
        
def fold_method(g):
    """method used when a player folds accepts the game then returns"""
    print("fold")
    g.new_game()
    g.game_pot=0
    return g
    
    
def play_game(g=game()):
    g.start_game()
    print("\n==================starting game===============\n")
    print("player 1 has: ",g.player1.bank," in the bank")
    print("player 2 has: ",g.player2.bank," in the bank")
    if g.is_training:
        t = training_element() #t is the training element which is used to track
        c1 = t.create_training_element(g.player2.card1)#remember player 2 is the computer
        c2 = t.create_training_element(g.player2.card2)
        t.add_hand(c1,c2)
    b = betting(g.player1,g.player2,g.to,0)
    x = b.decide()
    
    #FLOP
    if x[0] == 'call':
        print("==============Flop==================")
        print("the game pot is: ",g.game_pot)
        g.game_pot+=x[1]
        g.flop()
        if g.is_training:
            elements = []
            for c in g.CommunityCards:
                elements.append(t.create_training_element(c))
            t.add_flop(elements[0],elements[1],elements[2])
        
        print_cards(g.CommunityCards)
        b=betting(g.player1,g.player2,g.to,g.game_pot)
        x=b.decide()
    else:
        return fold_method(g)

    #TURN

    if x[0]=="call":
        g.game_pot=x[1]
        
        print("the game pot is: ",g.game_pot)
        print("=============TURN===================")
        g.turn()
        if g.is_training:
            t.add_turn(t.create_training_element(g.CommunityCards[-1]))
        for card in g.CommunityCards:
            print(card.value,card.suit)
        #print(g.to)
        b = betting(g.player1,g.player2,g.to,g.game_pot)
        x=b.decide()
        
    else:
        return fold_method(g)

    #RIVER

    if x[0]=="call":
        g.game_pot=x[1]
        print("the game pot is: ",g.game_pot)
        print("=============RIVER===================")
        g.river()
        if g.is_training:
            t.add_river(t.create_training_element(g.CommunityCards[-1]))
        for card in g.CommunityCards:
            print(card.value,card.suit)
        #print(g.to)
        b = betting(g.player1,g.player2,g.to,g.game_pot)
        x=b.decide()
        
    else:
        return fold_method(g)
        
    #Check Hands
    if x[0]=="call":
        g.game_pot=x[1]
        print("=============Checking Hands===================")
        print("pot: ", g.game_pot)
        Player1_Victory_ret = "Player1"
        Player2_Victory_ret = "Player2"
        Draw_ret = "Draw"
        x = g.check_hands()
        if x == Player1_Victory_ret:
            g.player1.bank+=g.game_pot
            #f.write('player1\n')
            if g.is_training:
                t.Outcome = 0 #will use 0 to indicate a loss
        elif x==Player2_Victory_ret:
            g.player2.bank+=g.game_pot
            #f.write('player2\n')
            if g.is_training:
                t.Outcome = 1 #will use 2 for a win
                       
        elif x==Draw_ret:
            g.player1.bank+=float(g.game_pot)/2
            g.player2.bank+=float(g.game_pot)/2
            #f.write('draw\n')
            if g.is_training:
                t.Outcome = 2 # will use 1 for a draw
        print(g.player1.bank,": Player 1")
        print(g.player2.bank,": Player 2")
        g.new_game()
        g.game_pot=0
        #g.deck.print_deck()
        if g.is_training:
                t.print_element()
                return [g,t]
        return g
    else:
        return fold_method(g)

g = game()
while True:
    
    g = play_game(g)

#all_training = []
#g.is_training=False
#g = play_game(g)

for i in range(10000):
    g=play_game(g)
    training = g[1]
    if training.Outcome!=2:
        all_training.append(training)
    g = g[0]
#for t in all_training:
#    t.print_element()
#f.close()
def start_training(all_training):

    model = keras.Sequential([
        #keras.layers.Input((17,1)),
        keras.layers.Dense(10,activation=tf.keras.activations.sigmoid)
        ,keras.layers.Dense(5,activation=tf.keras.activations.sigmoid)
        ,keras.layers.Dense(2,activation=tf.keras.activations.sigmoid)
        ])
    #add in the model informaiton for compling
    model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    labels = []
    training_examples = []
    for i in range(len(all_training)):
        t = all_training[i]
        labels.append(t.Outcome)
        training_examples.append(t.Hand)
    model.fit(np.array(training_examples),np.array(labels),epochs=10)
    print("hand done")
    training_examples = []
    new_labels = []
    for i in range(len(all_training)):
        y = all_training[i]
        x=(np.expand_dims(y.Hand,0))
        x= model.predict(x)
        if x[0][0]>0.5:
            new_training=[]
            tnt = y.Flop
            new_labels.append(labels[i])
            for x1 in tnt:
                new_training.append(x1)
            for x1 in x[0]:
                new_training.append(x1)
            training_examples.append(new_training)
        else:
            print(x)
    model = keras.Sequential([
        keras.layers.Dense(10,activation=tf.keras.activations.sigmoid)
        ,keras.layers.Dense(5,activation=tf.keras.activations.sigmoid)
        ,keras.layers.Dense(2,activation=tf.keras.activations.sigmoid)
        ])
    print(len(training_examples))
    print(float(sum(new_labels))/len(new_labels))
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    model.fit(np.array(training_examples),np.array(new_labels),epochs = 5)
    for x in model.weights:
        print(x)
    print(model.get_weights())
#start_training(all_training)

    
    
    
    #print(x)
    #print(labels[i])
    




"""
f = open('game_log.txt')
wld = [0,0,0]
for line in f:
    if line=='draw\n':
        wld[2]+=1
    elif line=='player1\n':
        wld[0]+=1
    elif line =='player2\n':
        wld[1]+=1
f.close()
print(float(wld[0])/sum((wld[0],wld[1])))
"""
#t = training_element()
#player1.card1 = card(7,'Diamond')
#player1.card2 = card(7,'Spade')
#print(t.create_training_element(player1.card1))


def test_game():
    player1 = player('p1')
    player2 = player('p2')
    player1.card1 = card(7,'Diamond')
    player1.card2 = card(7,'Spade')

    player2.card1 = card(8,'Diamond')
    player2.card2 = card(8,'Spade')

    c_cards = [card(2,'Heart'),card(3,'Heart'),card(4,'Heart'),card(10,'Diamond'),card(11,'Diamond')]

    new_game = game()
    new_game.CommunityCards=c_cards
    new_game.player1 = player1
    new_game.player2 = player2
    new_game.check_hands()








