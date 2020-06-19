#!/usr/bin/env python3
import sys
from Source.game import play
import Source.player_choices.cindy.model as cindy_model


def main():
    number_games = 10000
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
    model = cindy_model.load()
    data = cindy_model.load_data()
    [x_train, y_train] = cindy_model.parse_data(data)
    cindy_model.train(model, x_train, y_train)