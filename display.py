from flask import Flask, render_template
import sys
from collections import namedtuple
import re
app = Flask(__name__)
text = ''

def get_number(string):
    return re.findall(r"[-+]?\d*\.\d+|\d+", string)[-1]

def parse_game(text):
    Game = namedtuple('Game', ['hands', 'winner'])
    Hand = namedtuple('Hand', ['turns', 'player1', 'player2',])
    Turn = namedtuple('Turn', [ 'actions', 'cards', 'pot'])
    Player = namedtuple('Player', ['bank', 'cards'])
    games = []
    text = text.split('\n')
    i = 0
    while i < len(text):
        line = text[i]
        if 'new game' in line:
            games.append(Game([], []))
            i +=1
            continue
        if 'new hand' in line:
            p1_bank = get_number(text[i+1])
            p2_bank = get_number(text[i+2])
            p1_cards = text[i+3].split(':')[-1].split('|')
            p2_cards = text[i+4].split(':')[-1].split('|')
            games[-1].hands.append(Hand([],
                                        Player(p1_bank, p1_cards),
                                        Player(p2_bank, p2_cards)))
            i+=5
            continue
        if 'choice' in line:
            games[-1].hands[-1].turns.append({'choice': line})
            i +=1
            continue
        if '====' in line:
            games[-1].hands[-1].turns.append({'cards': text[i+3], 'pot': get_number(text[i+4])})
            i+=5
            continue
        if 'hand winner' in line:
            games[-1].hands[-1].turns.append({'winner': line})
            i +=1
            continue
        if 'game winner' in line:
            games[-1].winner.append(line)
            print(line)
            print(games[-1].winner)
            i +=1
            continue
        i +=1


    return games

@app.route('/')
def hello_world():
    print('hello')
    global text
    if not text:
        text = sys.stdin.read()
    #if not text:
    #    with open('example-input', 'r') as f:
    #        text = f.read()
    games=parse_game(text)
    return render_template('main.html', games=games)

if __name__ == '__main__':
    print('run')
    app.run(debug=False)





