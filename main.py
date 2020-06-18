#!/usr/bin/env python3
import sys
from Source.game import play
import Source.player_choices.player1.training1 as t


def train():
    t.train_model()


def main():
    number_games = 10
    if len(sys.argv) > 1:
        number_games = int(sys.argv[1])

    counter = {pn: 0 for pn in ('player 1', 'player 2')}
    for i in range(number_games):
        winner = play()
        print(winner)
        counter[winner] += 1
    print(counter)
    print(
        f'player 1 won {100*counter["player 1"]/(counter["player 1"]+counter["player 2"])}%'
    )


if __name__ == '__main__':
    main()
