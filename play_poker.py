from src.game import Game
from src.players import CheckCallPlayer, ConsolePlayer, GuiPlayer, RandomPlayer


def play_game(player1, player2):
    game = Game(player1, player2)
    num_games = 0
    while True:
        game.play_hand()
        num_games += 1
    print(f"number of games is: {num_games}")


if __name__ == "__main__":
    player1 = GuiPlayer("player 1", 1000)
    player2 = CheckCallPlayer("player 2", 1000)
    play_game(player1, player2)
