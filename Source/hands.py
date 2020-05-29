import numpy as np

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def card_string(self):
        if self.value == 1:
            cval = "Ace"
        elif self.value == 11:
            cval = "Jack"
        elif self.value == 12:
            cval = "Queen"
        elif self.value == 13:
            cval = "King"
        else:
            cval = self.value
        return f'{cval} of {self.suit}'

class Deck:
    suits = 'Hearts Diamonds Spades Clubs'.split()
    values = range(13)
    def __init__(self):
        # self.suits = 'Hearts Diamonds Spades Clubs'.split()
        # self.values = range(13)
        self.cards = [Card(suit, value) for suit in self.suits for value in range(1, 14)]

    def deal_card(self):
        return self.cards.pop()

    def shuffle(self):
        new_deck = []
        while len(self.cards)>0:
            new_deck.append(self.cards.pop(np.random.choice(range(0,len(self.cards)))))
        # assert len(new_deck) == 52
        self.cards = new_deck

    def __getitem__(self, item):
        return self.cards[item]


class HandMatrix:
    def __init__(self):
        self.hand_matrix = np.zeros(shape=(4,13))
        self.cards = []
    def add_card(self, card):
        self.cards.append(card)
        row = Deck.suits.index(card.suit)
        column = card.value - 1
        self.hand_matrix[row, column] += 1
    def reset_hand(self):
        self.hand_matrix = np.zeros(shape=(4,13))
        self.cards = []
    def get_hand_matrix(self):
        return self.hand_matrix

class Hand(HandMatrix):

    def __init__(self):
        super(Hand, self).__init__()

    def check_flush(self):
        suit_counts = np.matmul(self.hand_matrix, np.ones(13))
        max_suit = np.max(suit_counts)
        if max_suit <= 4:
            return False, None
        straight_check = np.array([1 if x == max_suit else 0 for x in suit_counts])
        projection = np.row_stack((np.matmul(np.transpose(self.hand_matrix),straight_check),np.zeros(shape=(3,13))))
        is_straight, hc = self.check_straight(projection)
        if is_straight:
            return True, {'type':'straight flush', 'high card': hc}
        else:
            _, hc = self.check_high_card(projection)
            return True, {'type': 'regular flush', 'high card': hc}

    def check_straight(self, to_check=None):
        if to_check is None:
            to_check = self.hand_matrix
        is_straight = False
        count = 0
        straight_checker = np.matmul(np.transpose(np.ones(4)),to_check)
        for i in range(len(straight_checker)+1):
            ind = i%len(straight_checker)
            if straight_checker[ind] > 0:
                count += 1
                if count > 4:
                    is_straight = True
            else:
                if is_straight:
                    return True, (ind - 1) %13
                else:
                    count = 0
        return is_straight, ind

    def check_pairs(self, to_check=None):
        if to_check is None: to_check = self.hand_matrix
        compress = np.matmul(np.transpose(np.ones(4)),to_check)

        # =========================================================================================
        # 4 of a kind
        # =========================================================================================
        if compress.max() == 4:
            return True, {'type':'four of a kind', 'hc': np.argmax(compress)}

        # =========================================================================================
        # full house
        # =========================================================================================
        # mask = [True if x == compress.max() and x != 0 else False for x in compress]
        # print(mask)
        elif (compress.max() == 3 and compress[[True if x != compress.max() and i != 0 else False for i,x in enumerate(compress)]].max() == 2) or (len(compress[compress==3])>1):
            mask = [True if x != compress.max() and i != 0 else False for i,x in enumerate(compress)]
            # print(compress[mask])
            to_ret = {'type': 'full house'}
            hc = {}
            if compress[0] > 1:
                if compress[0] == 3:
                    hc['triples'] = 0
                elif compress[0] == 2:
                    hc['pair'] = 0

            if compress.max() == 3 and compress[mask].max() == 2:
                for i, x in enumerate(np.flipud(compress)):
                    if x == 3:
                       hc['triples'] = len(compress) - i - 1
                    elif x == 2:
                        hc['pair'] = len(compress) - i - 1
            else:
                for i, x in enumerate(np.flipud(compress)):
                    if x == 3:
                        if 'triples' not in hc:
                            hc['triples'] = len(compress) - i - 1
                        else:
                            hc['pair'] = len(compress) - i - 1
                            break
            to_ret['hc'] = hc
            return True, to_ret

        # =========================================================================================
        # three of a kind
        # =========================================================================================
        elif compress.max() == 3:
            return True, {'type':'three of a kind', 'hc':np.argmax(compress)}
        # =========================================================================================
        # two pair
        # =========================================================================================
        elif len(compress[compress==2])>1:
            to_ret = {'type': 'two pair'}
            hc ={}
            if compress[0] > 1:
                hc['top_pair'] = 0
            for i, x in enumerate(np.flipud(compress)):
                if x == 2:
                    if 'top_pair' in hc:
                        hc['bottom_pair'] = len(compress) - i - 1
                        to_ret['info'] = hc
                        return True, to_ret
                    else:
                        hc['top_pair'] = len(compress) - i - 1

        # =========================================================================================
        # Pair
        # =========================================================================================
        elif compress.max() == 2:
            return True ,{'type': 'pair', 'hc': np.argmax(compress)}
        return False, None

    def check_high_card(self,to_check=None):
        if to_check is None: to_check = self.hand_matrix
        compress = np.matmul(np.transpose(np.ones(4)),to_check)
        if compress[0] > 0:
            return True, 0
        else:
            for i,x in enumerate(np.flipud(compress)):
                if x>0:
                    return True, len(compress) - i - 1

    def check_hand(self):

        # Flush Checker
        check, hc = self.check_flush()
        if check:
            hand = hc['type']
            high_card = hc['high card']
            # if high_card == 0: high_card = 13
            self.hand_info = {'hand':hand, 'high_card': high_card}
            return self.hand_info
        # straight
        # you can't have anything in pairs that beats a straight and a straight... so checking in this order is fine...
        # I think?
        check, hc = self.check_straight()
        if check:
            # if hc == 0: hc = 13
            self.hand_info = {'hand':'straight', "high_card":hc}
            return self.hand_info
        # pairs
        check, hc = self.check_pairs()
        if check:
            self.hand_info = {'hand':hc['type'], 'info':hc}
            return self.hand_info
        # high card
        check, hc = self.check_high_card()
        self.hand_info = {'hand': 'high card', 'high_card': hc}
        return self.hand_info


def test_hand(hand, expected=None):
    han = Hand()
    for x in hand:
        han.add_card(x)
    x = han.check_hand()
    print(f'actual: {x}')
    print(f'expected: {expected}')

 # King of Hearts | 10 of Diamonds | 7 of Clubs | Jack of Diamonds | 7 of Hearts | 10 of Spades | 2 of Spades
if __name__ == '__main__':

    full_house = [Card('Spades',1), Card('Diamonds',1), Card('Hearts',1), Card('Diamonds',6), Card('Spades',3), Card('Spades',6), Card('Clubs',6)]
    three_of_a_kind = [Card('Spades',1), Card('Diamonds',1), Card('Hearts',4), Card('Diamonds',6), Card('Spades',3), Card('Spades',6), Card('Clubs',6)]
    flush_three_of_a_kind = [Card('Spades',13), Card('Spades',2), Card('Spades',4), Card('Diamonds',6), Card('Spades',3), Card('Spades',6), Card('Clubs',6)]
    four_of_a_kind = [Card('Spades', 13), Card('Spades', 2), Card('Hearts', 6), Card('Diamonds', 6),
                             Card('Spades', 3), Card('Spades', 6), Card('Clubs', 6)]
    two_pair = [Card("Hearts", 13), Card("Diamonds", 10), Card("Clubs", 7), Card("Diamonds", 11), Card("Hearts", 7),
              Card("Spades", 10), Card("Spades", 2)]
    test_hand(full_house, 'full house')
    test_hand(three_of_a_kind,'three of a kind')
    test_hand(flush_three_of_a_kind, 'flush')
    test_hand(four_of_a_kind, '4 of a kind')
    test_hand(pair_7, "two pair")

