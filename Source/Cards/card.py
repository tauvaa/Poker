#!/usr/bin/python3

from tkinter import *
# from PIL import Image
# from Source.game import card

def add_hand(parent,card1,card2,offset=2):
        """
        function used to create a with the hand give the parent frame it returns the parent with the info in it
        """
        c1 = card_frame(parent)
        c2 = card_frame(parent)
        c1.add_card(card1)
        c2.add_card(card2)
        c1.add_labels(parent,offset=offset)
        c2.add_labels(parent,cl=2,offset=offset)
        #b=Button(parent,text='click me',command=parent.destroy)
        #b.grid(row=10,column=1)
        return parent
def add_flop(parent,flop,offset=0):
    """Function which takes in a parent and flop (list of 3 cards) it then returns
    a frame with the flop"""
    
    count = 1
    for c in flop:
        c1 = card_frame(parent)
        c1.add_card(c)
        c1.add_labels(parent,cl=count,offset=offset)
        count+=1 #add 1 to count to shift the row
    return parent
    



class card_frame(Frame):
    
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master #top level master frames used when you need to destroy frames
        self.current = Frame(self.master) #current frame to add labels and stuff to - should probably move this to a method at some point
        #self.value=7
        #self.suit='Diamond'
        #self.add_labels()
        self.current.grid()
        #Label(self.current,text='hello world').grid()
    def add_card(self,card):
        self.card = card
        self.value = card.value
        self.suit = card.suit
    def add_labels(self,parent,cl=1,offset=0):
        #to_ret = Frame(parent)
        lab_suit = Label(parent,text = self.suit)
        lab_value = Label(parent,text=str(self.value))
        #image = Image.open("test")
        if self.suit=='Diamond':
            picture = PhotoImage(file='Source/Cards/diamond.gif')
        elif self.suit =='Club':
            picture = PhotoImage(file='Source/Cards/club.gif')
        elif self.suit =='Spade':
            picture = PhotoImage(file='Source/Cards/spade.gif')
        elif self.suit =='Heart':
            picture = PhotoImage(file='Source/Cards/heart.gif')
        else:
            picture = PhotoImage(file='test.gif')
        
        #picture.grid(row=1,colum=3)
        # print(type(picture))
        #photo = PhotoImage(picture)
        lab_photo=Label(parent,image=picture)
        lab_photo.image=picture
        #lab_suit.grid(row=1,column=2)
        #return self.current
        lab_photo.grid(row=2+offset,column=cl)
        lab_value.grid(row=1+offset,column=cl)
        #parent.grid(row=1,column=cl)
        #self.current.grid()
    
        
    
def main():
    root = Tk()
    root.geometry('600x600')
    hand = Frame(root)
    #flop_frame = Frame(root)
    #c = card_frame(temp)
    
    #c1 = card_frame(temp)
    #c2 = card_frame(temp)
    #c1.grid(row=1,column=1)
    #c2.grid(row=1,column=2)
    card1 = card(10,'Spade')
    card2 = card(7,'Heart')
    card3 = card(6,'Diamond')
    flop =  [card1,card2,card3]
    #flop = add_flop(flop_frame,flop)
    #flop.grid(row=1,column=1)
    
    hand = add_hand(hand,card1,card2)
    hand = add_flop(hand,flop)
    hand.grid()
    hand.mainloop()
    #root.grid()
    #hand.grid(row=2,column=2)
    #root.mainloop()
    #c1.add_card(card1)
    
    #c1.add_labels(temp)
    #c2.add_card(card2)
    #c2.add_labels(temp,cl=2)
    #print(f1)
    #c.grid(row=1,column=1)
    #temp.mainloop()
    #c= card()
    #c.add_labels()
# main()

        
        
        
    

