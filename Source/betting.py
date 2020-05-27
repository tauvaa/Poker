#!/usr/bin/python3


"""This is the modulo file for the betting in the poker game"""

import tkinter as tk
from .Cards.card import add_hand,add_flop
_SCREEN_GEOMETRY_= '600x600'
def read_player_input(b):
    #d=""
    
        #B1 = tk.Button(popupBonusWindow, text="Okay", command=popupBonusWindow.destroy)
        #B1.grid(row=1,column=0)
    # popupBonusWindow.mainloop()
    #print(d)
    #to_ret = x.mainloop()
    #return d
    if b.is_training:
        return 'x'
    else:
        #return 'b'
        put = input("what would you like to do? You can check (x) or bet (b)\n")
        return put
    
class betting:
    
    def __init__(self,player1,player2,to,pot,is_training,model=None,indp_var=None):
        #remember in the to variable 0 = player2 1 = player1
        self.player1 = player1
        self.player2 = player2
        self.back_to = to
        self.to=to
        self.pot = pot
        self.previous_decision = None
        self.to_call = 0 #the ammount that is needed to call
        self.is_training = is_training
        self.model = model #this is the model which will be used to make decisions
        self.indp_var = indp_var# this is the vector which gets passed to betting (is the cards vector)
        print("the pot currently is",self.pot)
    def switch_player(self):
        if self.to==1:
            self.to=0
        else:
            self.to=1
    def popup(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.geometry(_SCREEN_GEOMETRY_)
        popupBonusWindow.wm_title("Decision Popup")
        labelBonus = tk.Label(popupBonusWindow, text="Input")
        labelBonus.grid(row=0, column=0)
        
        def check_command():
            #self.check()
            self.decision='x'
            popupBonusWindow.destroy()
            #return d
        def call_command():
            #global d
            #self.call_hand()
            self.decision='c'
            popupBonusWindow.destroy()
            #return 'c'
            
        def fold_command():
            self.decision= 'f'
            popupBonusWindow.destroy()
        def bet_command():
            self.decision = 'b'
            popupBonusWindow.destroy()

        call_button = tk.Button(popupBonusWindow,text='call',command=lambda:call_command())
        call_button.grid(row=1,column=0) 
        check_button = tk.Button(popupBonusWindow,text='check',command=lambda:check_command())
        check_button.grid(row=1,column=1)
        fold_button = tk.Button(popupBonusWindow,text='fold',command=lambda:fold_command())
        fold_button.grid(row=1,column=2)
        bet_button = tk.Button(popupBonusWindow,text='bet',command=lambda:bet_command())
        bet_button.grid(row=1,column=3)
        return popupBonusWindow



            
            
    def computer_choice(self):
        if self.is_training:
            return 'c'
        
        pred = self.model.predict(self.indp_var)
        if self.previous_decision!='b':
            if pred[0]>0.34:
                decision = 'b'
            else:
                decision='x'
        else:
            #self.player2.show_cards()
            #print(pred)
            
            #return 'c'
            if pred[0]>0.3:
                if pred[0]>0.34:
                    decision='b'
                else:
                    decision = 'c'
            else:
                decision = 'f'
        return decision
    
    
    def decide(self):
        """function which decideds which method to call"""
        print(f'player 1 bank: {self.player1.bank}')
        print(f'player 1 bank: {self.player2.bank}')
        if self.to==1:
            self.player1.show_cards()
            # decision=read_player_input(self)
            x = self.popup()
            x.mainloop()
            decision = self.decision
        else:
            decision = self.computer_choice()
        if decision=='x':
            if self.previous_decision=='b':
                print('cannot check, bet or fold option only')
                return self.decide()
            return self.check()
        elif decision=='c':
            return self.call_hand()
        elif decision=='b':
            #add in something to get how much to bet
            #print("bet")
            return self.bet(25)
        elif decision=='f':
            return self.fold()
        else:
            print(decision +" option could no be found, please use on of x,b,c,f")
            return self.decide()
        
    
    
    def exit_betting(self,exit_condition):
        """this function will be used to exit betting and continue the game"""
        print("==================end of betting round===================")
        if exit_condition == 'f':
            return ['fold',0]
        else:
            self.to=self.back_to
            print("exited with call")
            return ['call',self.pot]
        
            
        
        
    
        
        
    def check(self):
        print("==========CHECK==========")
        if self.previous_decision=='x':
            return self.exit_betting('c')
        else:
            self.previous_decision='x'
            self.switch_player()
            return self.decide()
        
    def bet(self,ammount):
        print("========BET==========")
        bet_amount = ammount + self.to_call
        self.pot+= bet_amount
        print("with that bet the pot is at: ", self.pot)
        self.to_call = ammount
        if self.to==1:
            self.player1.bank -= bet_amount
        else:
            self.player2.bank -= bet_amount
        self.switch_player()
        print(self.to,' to')
        self.previous_decision='b'
        return self.decide()
        
        
    def call_hand(self):
        print("==========CALL=========")
        if self.to == 1:
            self.pot+=self.to_call
            self.player1.bank-=self.to_call
            print("player 1 has called")
        else:
            self.pot+=self.to_call
            self.player2.bank-=self.to_call
            print("player 2 has called")
            #print("player 2 ", self.to_call)
        self.to_call=0
            
        print("with that call the pot is at: ",self.pot)
        return self.exit_betting('c')
        
    def fold(self):
        print(self.previous_decision)
        if self.to==1:
            self.player2.bank+=self.pot
        else:
            self.player1.bank+=self.pot
        return self.exit_betting('f')
    
    



