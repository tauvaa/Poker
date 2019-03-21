#!/usr/bin/python3


"""
Python poker application
20190218 - created ui call, check, fold buttons
"""

_SCREEN_GEOMETRY_= '600x600'
#================Libraries=================
import tkinter as tk
import random
from Source.game import *
from Source.betting import *
from Source.learning_mod import *
from Source.Cards.card import *
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras




class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.master_frame=master
        self.current_frame=tk.Frame(master)
        self.deck = deck()
        self.player1 = None #this is the human player
        self.player2 = None #this is the computer player
        tk.Button(self.current_frame,text='click',command=self.start_game).grid(row=1,column=1)
        self.current_frame.grid()
        self.game=game()
    def card_frame(self,master,card):
        """this method can be used to make a frame for each card"""
        card_frame = tk.Frame(master)
        if card.suit in ['Diamond','Heart']:
            f = tk.Frame(card_frame,bg='red',height=10,width=20).grid(row=1,column=1)
        else:
            f=tk.Frame(card_frame,bg='black',height=10,width=20).grid(row=1,column=1)
        suit = card.suit
        if card.value == 1:
            value ="Ace"
        elif card.value == 11:
            value = 'Jack'
        elif card.value == 12:
            value = 'Queen'
        elif card.value ==13:
            value = 'King'
        else:
            value = str(card.value)
        #tk.Label(card_frame).grid(row=1,column=1)
        tk.Label(card_frame,text=value,anchor='w').grid(row=2,column=1)
        tk.Label(card_frame,text=suit,anchor='w').grid(row=3,column=1)
        
        
        return card_frame
    
    def start_game(self):
        """ this is what will be used to start the game
        will deal 2 cards to each player"""
        
        #first we need to make sure both players are playing
        new_frame = tk.Frame()
        self.current_frame.destroy()
        self.current_frame=new_frame        
        if self.player1==None:
            self.player1=player('Tolo')
        if self.player2==None:
            self.player2=player('Computer')
        
        
        #now we need to shuffle the cards
        self.deck.shuffle()

        #now we need to deal
        self.player1.card1=self.deck.cards.pop()
        self.player2.card1=self.deck.cards.pop()
        self.player1.card2=self.deck.cards.pop()
        self.player2.card2=self.deck.cards.pop()
        self.game.add_players(self.player1,self.player2)
        #make the players cards
        f_player2 = tk.Frame(self.master_frame)
        f_player1 = tk.Frame(self.master_frame)
        self.card_frame(f_player2,self.player2.card1).grid(row=1,column=1,padx=5,pady=5)
        self.card_frame(f_player2,self.player2.card2).grid(row=1,column=2,padx=5,pady=5)
        self.card_frame(f_player1,self.player1.card1).grid(row=1,column=1,padx=5,pady=5)
        self.card_frame(f_player1,self.player1.card2).grid(row=1,column=2,padx=5,pady=5)
        f_player2.grid(row=1,column=1)
        f_player1.grid(row=3,column=1)
        
        #make the command (call,pass,fold)
        commands = tk.Frame(self.master_frame)
        tk.Button(commands,text='check',command=self.check).grid(row=1,column=1)
        tk.Button(commands,text='call').grid(row=1,column=2)
        tk.Button(commands,text='fold').grid(row=1,column=3)
        tk.Button(commands,text='click',command=self.start_game).grid(row=2,column=1)
        self.commands=commands
        self.commands.grid(row=4,column=1)
        
    def check(self):
        """ function can be use to check in game"""
        if self.game.state == 'preflop':
            new_frame = tk.Frame(self.master_frame)
            for i in range(3):
                new_card = self.deck.cards.pop()
                self.game.add_card(new_card)
                c = self.card_frame(new_frame,new_card)
                c.grid(row=1,column=1+i,padx=5)
            new_frame.grid(row=2,column=1,padx=5)
            self.CommunityCards=new_frame
            self.game.state ='preturn'

        elif self.game.state=='preturn':
            self.deck.cards.pop() #burn 1
            new_card=self.deck.cards.pop()
            c = self.card_frame(self.CommunityCards,new_card)
            self.game.add_card(new_card)
            c.grid(row=1,column=4,padx=5)
            self.game.state='preriver'
            #self.CommunityCards=c

        elif self.game.state =='preriver':
            new_card = self.deck.cards.pop()
            c = self.card_frame(self.CommunityCards,new_card)
            c.grid(row=1,column=5,padx=5)
            self.game.add_card(new_card)
            self.game.check_hands()
            self.game.state = 'DONE'
        
        
                
def full_game():
    #g = game()
    #g.is_training = True
    #g.player1.bank = 10000
    #g.player2.bank = 10000
    #g.initalize_models()
    x =create_training_set(1000)
    print("training set complete")
    g = game()
    g.initalize_models(x)
    g.ui='gui'
    #outcomes = []
    while True:
        f = Tk()
        f.geometry('600x600')
        if g.player1.bank<0:
            print("player 2 won")
            return 'player2'
            break
        elif g.player2.bank<0:
            print("player 1 won")
            return 'player1'
            break
        
        g = play_game(g,f)
    
def main():
    full_game()
    """try:
        full_game()
    except:
        full_game()"""
main()
    
"""
def main():
    print("hello world")
    c = deck()
    c.shuffle()
    c.print_deck()
    root = tk.Tk()
    root.geometry("500x500")
    app = Application(root)
    app.mainloop()
main()

"""
