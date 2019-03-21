"""
module to store the game code

2019-02-21: Added a get training set funciton

"""
_SCREEN_GEOMETRY_= '600x600'

import random
from Source.betting import *
from .learning_mod import *
from .Cards.card import *
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
    
    


class deck:
    def __init__(self):
        self.cards = []
        suits = ('Diamond','Club','Spade','Heart')
        card_number = 1
        suit_number = 0
        for i in range(52):
            c = card(card_number,suits[suit_number])
            self.cards.append(c)
            card_number+=1
            if i>0 and (i+1)%13==0:
                suit_number+=1
                card_number = 1
    def new_deck(self):
        self.cards = [] #intiallize the cards to 0
        suits = ('Diamond','Club','Spade','Heart')
        card_number = 1
        suit_number = 0
        for i in range(52):
            c = card(card_number,suits[suit_number])
            self.cards.append(c)
            card_number+=1
            if i>0 and (i+1)%13==0:
                suit_number+=1
                card_number = 1
        
    def print_deck(self):
        for card in self.cards:
            print(card.value,card.suit)
    def shuffle(self):
        old_array = self.cards
        
        new_array = []
        for i in range(52):
            if len(old_array)==1:
                index=0
            else:
                index = random.randint(0,len(old_array)-1)
            #print(len(old_array))
            #print(index, i)
            new_value=old_array.pop(index)
            new_array.append(new_value)
            #old_array.drop(index)
        self.cards =new_array
        #check to make sure you have 52 cards
        if len(self.cards)!=52:
            raise ValueError("52CardsReqAfterShuffle")
    
class card:
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit
    
            


class player:
    def __init__(self,playerName):
        self.bank = 1000 #start the game with $1000
        self.player_name = playerName
        self.card1 = None
        self.card2 = None
    def lose_cards():
        self.card1=None
        self.card2=None
    def show_cards(self):
        """function used to show the players cards
        will print them to standard output"""
        x = [self.card1,self.card2]
        for i in x:
            print(i.value,' ',i.suit)
        

class game:
    def __init__(self):
        #state is used to track where the game is at will have to change as game progresses
        self.state=None
        self.deck = deck() #deck that will be used for the game
        self.CommunityCards = [] #these are the flop, turn and river
        self.player1 = player('Person')
        self.player2 = player('Computer')
        #set who the dealer is
        self.dealer=1 #computer deals first
        self.to=0#indicator variable to say who the game is waiting on input from (0 is player2 1 is player1)
        self.game_pot = 0 #game pot gets added to as the rounds advance
        self.is_training = False # indicator varialbe to tell the game if you are training or not
        self.preFlop_model = None
        self.flop_model = None
        self.turn_model = None
        self.river_model = None
        self.ui=None #will be used to indicate which ui to use None -> stdout, gui -> TkInter
    def initalize_models(self,training_set):
        #training_set = create_training_set()
        self.preFlop_model = model_training(training_set,'Hand')

        self.flop_model = model_training(training_set,'Flop')

        self.turn_model = model_training(training_set,'Turn')

        self.river_model = model_training(training_set,'River')
        
        
        
    def switch_dealer():
        if self.dealer==1:
            self.dealer=0
        else:
            self.dealer=1
    def new_game(self):
        """
        method used to start a new game, will initalize the community cards, create a new deck, suffle it and set the players cards
        """
        self.deck.new_deck()
        #self.deck.print_deck()
        self.player1.card1=None
        self.player1.card2=None
        self.player2.card1=None
        self.player2.card2=None
        self.CommunityCards = []
        
        
        
        
    
    def start_game(self):
        """method used to start a game.  Will shuffle the game
        deck and deal cards."""
        #shuffle the deck
        self.deck.shuffle()
        #deal the cards
        if self.dealer==0:
            
            self.player1.card1=self.deck.cards.pop()
            self.player2.card1=self.deck.cards.pop()
            self.player1.card2=self.deck.cards.pop()
            self.player2.card2=self.deck.cards.pop()
        else:
            self.player2.card1=self.deck.cards.pop()
            self.player1.card1=self.deck.cards.pop()
            self.player2.card2=self.deck.cards.pop()
            self.player1.card2=self.deck.cards.pop()
    
            
    def flop(self):
        #add three cards to the community cards
        for i in range(3):
            self.add_card(self.deck.cards.pop())
    def turn(self):
        #burn and turn
        self.deck.cards.pop()
        self.add_card(self.deck.cards.pop())
    def river(self):
        self.add_card(self.deck.cards.pop())
        
        
    def add_card(self,card):
        """ function which can be used to add cards to the community cards"""
        self.CommunityCards.append(card)
        
    def check_hands(self):
        HANDS=['high card','pair','two pair','three of a kind','straight','full house','flush','four of a kind'\
            ,'straight flush','royal flush']
        
        def check_player(player):
            
            def check_straight(cards):
                v =[]
                for c in cards:
                    v.append(c.value)
                v.sort
                if v[0]==1:
                    v.append(14)
                streak=0
                for x in range(len(v)):
                    streak+=1
                    if x+1>=len(v):
                        break
                    else:
                        if v[x+1]!=v[x]+1:
                            streak=0
                    if streak>4:
                        return True
                if streak>4:
                    return True
                else:
                    return False
                
                
            def check_pairings(cards):
                """Function used to check the card pairings,
                So will return an array with each element of the form [value,number found]"""
                def value_exist(array,v):
                    #returns a bool indicating if the pairing is in the cards
                    #also returns and index
                    for i in range(len(array)):
                        x=array[i]
                        if x[0]==v:
                            return [True,i]
                    return [False,-1]
                values = []
                for c in cards:
                    cp = value_exist(values,c.value)
                    if cp[0]:
                        values[cp[1]][1]+=1
                    else:
                        values.append([c.value,1])
                return values
            
            def check_four_kind(value_array):
                for x in value_array:
                    if x[1]>=4:
                        return True
                return False
            def check_three_kind(value_array):
                for x in value_array:
                    if x[1]>=3:
                        #print(x)
                        return True
                return False
            def check_pair(value_array):
                for x in value_array:
                    if x[1]==2:
                        return True
                return False
            def check_two_pair(value_array):
                one_pair = False
                for x in value_array:
                    if x[1]==2:
                        if one_pair == True:
                            return True
                        else:
                            one_pair = True
                return False
                
            cards = self.CommunityCards.copy()
            cards.append(player.card1)
            cards.append(player.card2)
            #print(self.CommunityCards)
            #check for a flush
            suit_totals={'Diamond':0,'Spade':0,'Club':0,'Heart':0}
            for x in cards:
                suit_totals[x.suit]+=1
                
            retvalue = "testing"#value which can be use to pass through return fucntion 
            
            
            if max(suit_totals.values())>4:
                #print("You have a flush")
                is_straight=check_straight(cards)
                if is_straight:
                    #print("you have a straight flush")
                    to_ret_string= 'straight flush'
                else:
                    to_ret_string= 'flush'
            else:
                #print("You do not have a flush")
                is_straight=check_straight(cards)
                if is_straight:
                    #print("you have a straight")
                    to_ret_string='straight'
                
                else:
                    pairing = check_pairings(cards)
                    #print(pairing)
                    revalue=pairing
                    value="forTesting" #get rid of this after testing
                    if check_four_kind(pairing):
                        to_ret_string='four of a kind'
                    elif check_three_kind(pairing):
                        to_ret_string= 'three of a kind'
                    elif check_pair(pairing):
                        #print("you have a pair")
                        #print("here")
                        if check_two_pair(pairing):
                            #print("you have two pair")
                            to_ret_string='two pair'
                        else:
                            to_ret_string='pair'
                            retvalue=pairing
                    else:
                        #print("you have a high card")
                        to_ret_string='high card'
                        retvalue = pairing #return the pairing in case of tie
            return [to_ret_string,retvalue]
        p1 = check_player(self.player1)
        p2 = check_player(self.player2)
        player1_hand = p1[0]
        print("Player 1 has "+player1_hand)
        print("Player 1 Hand")
        self.player1.show_cards()
        player1_draw_info =p1[1] 
        player2_hand = p2[0]
        print("Player 2 has "+player2_hand)
        print("Player 2 Hand")
        self.player2.show_cards()
        print("the Community Cards are")
        print_cards(self.CommunityCards)
        
        player2_draw_info = p2[1]
        def rank_hand(h):
            hand_found=False
            for i in range(len(HANDS)):
                hand=HANDS[i]
                if h==hand:
                    hand_found=True
                    rank=i
                    break
            if hand_found:
                
                return rank
            else:
                raise NameError('HandNotFound')
        player1_handRank = rank_hand(player1_hand)
        player2_handRank = rank_hand(player2_hand)
        
        #Static return values
        Player1_Victory_ret = "Player1"
        Player2_Victory_ret = "Player2"
        Draw_ret = "Draw"
        #values to print to console
        Player1_Victory = "The winner is player 1"
        Player2_Victory = "The winner is player 2"
        if player1_handRank>player2_handRank:
            print(Player1_Victory)
            return Player1_Victory_ret
        elif player1_handRank<player2_handRank:
            print(Player2_Victory)
            return Player2_Victory_ret
        else:
            #print(player1_handRank)
            if player1_handRank==0: #for when both players have a high card
                def get_high_card(pairing):
                    temp = []
                    for c in pairing:
                        temp.append(c[0])
                    if min(temp)==1:
                        return 14
                    else:
                        return max(temp)
                p1 = get_high_card(player1_draw_info)
                p2 = get_high_card(player2_draw_info)
                if p1>p2:
                    print(Player1_Victory)
                    return Player1_Victory_ret
                elif p1<p2:
                    print(Player2_Victory)
                    return Player2_Victory_ret
                else:
                    print("the game is a draw, High card")
                    return Draw_ret
                
            if player1_handRank==1:
                """This is when it is a pair"""
                def find_high_card(pairings):
                    for x in pairings:
                        if x[1]==2:
                            #this is to check if you have a pair of aces
                            if x[0]==1:
                                return 14
                            return x[0]                
                p1_highCard = find_high_card(player1_draw_info)
                p2_highCard = find_high_card(player2_draw_info)
                if p1_highCard>p2_highCard:
                    print(Player1_Victory)
                    return Player1_Victory_ret
                elif p2_highCard>p1_highCard:
                    print(Player2_Victory)
                    return Player2_Victory_ret
                else:
                    print("game is a draw")
                    return Draw_ret
            else:
                return Draw_ret
        print("player 1 "+player1_hand)
        print("player 2 "+player2_hand)


def play_game(g=game(),master=None):
    g.start_game()
    print("\n==================starting game===============\n")
    print("player 1 has: ",g.player1.bank," in the bank")
    print("player 2 has: ",g.player2.bank," in the bank")
    #if g.is_training:
    t = training_element() #t is the training element which is used to track
    c1 = t.create_training_element(g.player2.card1)#remember player 2 is the computer
    c2 = t.create_training_element(g.player2.card2)
    t.add_hand(c1,c2)
    #m1 = master
    hand_text="Hi, welcome to Poker. You're hand is below, click betting when you are ready to begin"
    if  g.ui=='gui':
        f = Frame(master)
        card1 = g.player1.card1
        card2 = g.player1.card2
        hand = add_hand(f,card1,card2)
        l =Label(text=hand_text)
        b = Button(f,text='Betting',command=master.destroy)
        l.grid(row=1,column=1)
        b.grid(row=100,column=1)
        hand.grid(row=2,column=1)
        f.mainloop()
    
    
    
    #else:
    #    t = training_element()
    #    c1 = t.create_training_element(g.player2.card1)
    #    c2 = t.create_training_element(g.player2.card2)
    print("HERE 123213")
    indp_var = t.Hand 
    b = betting(g.player1,g.player2,g.to,0,g.is_training,g.preFlop_model,indp_var)#zero is the pot
    x = b.decide()
    
    #FLOP
    if x[0] == 'call':
        print("==============Flop==================")
        print("the game pot is: ",g.game_pot)
        g.game_pot+=x[1]
        g.flop()
        #if g.is_training:
        elements = []
        for c in g.CommunityCards:
            elements.append(t.create_training_element(c))
        t.add_flop(elements[0],elements[1],elements[2])
        
        print_cards(g.CommunityCards)
        if  g.ui=='gui':
            master = Tk()
            master.geometry(_SCREEN_GEOMETRY_)
            f = Frame(master)
            card1 = g.player1.card1
            card2 = g.player1.card2
            
            hand = add_hand(f,card1,card2)
            hand = add_flop(hand,g.CommunityCards)
            b = Button(f,text='click me',command=master.destroy)
            b.grid(row=5,column=1)
            hand.grid(row=1,column=1)
            f.mainloop()
        
        #t = training_element()
        #c1 = t.create_training_element(g.player2.card1)
        #c2 = t.create_training_element(g.player2.card2)
        #temp = np.zeros(len(c1))
        #for i in g.CommunityCards:
        #    temp+=t.create_training_element(i)
        
        #indp_var = c1+c2+temp
        indp_var = t.Hand+t.Flop
        
        b=betting(g.player1,g.player2,g.to,g.game_pot,g.is_training,g.flop_model,indp_var)
        x=b.decide()
    else:
        return fold_method(g)

    #TURN

    if x[0]=="call":
        g.game_pot=x[1]
        print("=============TURN===================")
        print("the game pot is: ",g.game_pot)
        g.turn()
        #if g.is_training:
        t.add_turn(t.create_training_element(g.CommunityCards[-1]))
        for card in g.CommunityCards:
            print(card.value,card.suit)
        if  g.ui=='gui':
            #sys.exit()
            master = Tk()
            f = Frame(master)
            card1 = g.player1.card1
            card2 = g.player1.card2
            
            hand = add_hand(f,card1,card2)
            hand = add_flop(hand,g.CommunityCards)
            b = Button(f,text='click me',command=master.destroy)
            b.grid(row=5,column=1)
            hand.grid(row=1,column=1)
            f.mainloop()
        #print(g.to)
        """t = training_element()
        c1 = t.create_training_element(g.player2.card1)
        c2 = t.create_training_element(g.player2.card2)
        temp = np.zeros(len(c1))
        for i in g.CommunityCards:
            temp+=t.create_training_element(i)
        indp_var = c1+c2+temp"""
        indp_var = t.Hand+t.Flop+t.Turn
        b = betting(g.player1,g.player2,g.to,g.game_pot,g.is_training,g.turn_model,indp_var)
        x=b.decide()
        
    else:
        return fold_method(g)

    #RIVER

    if x[0]=="call":
        g.game_pot=x[1]
        
        print("=============RIVER===================")
        print("the game pot is: ",g.game_pot)
        g.river()
        #if g.is_training:
        t.add_river(t.create_training_element(g.CommunityCards[-1]))
        for card in g.CommunityCards:
            print(card.value,card.suit)
        if  g.ui=='gui':
            #sys.exit()
            master = Tk()
            f = Frame(master)
            card1 = g.player1.card1
            card2 = g.player1.card2
            
            hand = add_hand(f,card1,card2)
            hand = add_flop(hand,g.CommunityCards)
            b = Button(f,text='click me',command=master.destroy)
            b.grid(row=5,column=1)
            hand.grid(row=1,column=1)
            f.mainloop()
        #print(g.to)
        """t = training_element()
        c1 = t.create_training_element(g.player2.card1)
        c2 = t.create_training_element(g.player2.card2)
        temp = np.zeros(len(c1))
        for i in g.CommunityCards:
            temp+=t.create_training_element(i)"""
            
        indp_var = t.Hand+t.Flop+t.Turn+t.River
        b = betting(g.player1,g.player2,g.to,g.game_pot,g.is_training,g.river_model,indp_var)
        x=b.decide()
        
    else:
        return fold_method(g)
        
    #Check Hands
    if x[0]=="call":
        g.game_pot=x[1]
        print("=============Checking Hands===================")
        print("The game pot is: ", g.game_pot)
        Player1_Victory_ret = "Player1"
        Player2_Victory_ret = "Player2"
        Draw_ret = "Draw"
        x = g.check_hands()
        def hand_ui(game=g,outcome=x):
            master = Tk()
            master.geometry('200x200')
            f = Frame(master)
            if outcome==Draw_ret:
                l = Label(f,text="Draw")
            elif outcome==Player1_Victory_ret:
                l = Label(f,text="Player Win!")
            else:
                l = Label(f,text="Computer Win")
            #l.padx=100
            b = Button(f,text="Play again",command=master.destroy)
            l.grid(row=1)
            b.grid(row=2)
            return f
        if g.ui == 'gui' and not g.is_training:
            frame = hand_ui()
            frame.grid()
            frame.mainloop()
                
            
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
                t.Outcome = 0 # will use 0.5 for a draw
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
    
def create_training_set(num_examples=1000):
    g = game()
    g.is_training=True
    to_ret = []
    for i in range(num_examples):
        g = play_game(g)
        training = g[1] #this is a training element
        to_ret.append(training)
        g = g[0] # the play game returns a array [game, training element]
    return to_ret

        
        
        
        
        
        
        
        
        
        
        