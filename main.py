#!/usr/bin/env python3
import sys
from Source.game import play
import Source.player_choices.player1.training as t
from Source.player_choices.player1.scratch import get_values, all_data
def play_games(ngames=10):
    # for _ in range(ngames):
    #     if len(sys.argv) > 1:
    #         number_games = int(sys.argv[1])

    counter = {pn: 0 for pn in ('player 1', 'player 2')}
    for i in range(ngames):
        winner = play()
        print(winner)
        counter[winner] += 1
    # print(counter)
    # print(f'player 1 won {100 * counter["player 1"] / (counter["player 1"] + counter["player 2"])}%')
    return counter
    # if counter['player 1'] > counter['player 2']:
    #     return 'player 1'
    # else:
    #     return 'player 2'

def main():
    # t.train_test()
    # number_games = 1
    ct = play_games(25)
    print(ct)
    print(f'player 1 won {100 * ct["player 1"] / (ct["player 1"] + ct["player 2"])}%')

    # get_values(all_data=all_data,percentile=.1, state='river')

    # play()
if __name__ == '__main__':
    main()
    # print(all_data)

