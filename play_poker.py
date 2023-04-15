from src.game import Game
from src.players.random_player import RandomPlayer
from src.players.console_player import ConsolePlayer

def play_game(player1, player2):
    game = Game(player1, player2)
    num_games = 0
    while True:
        winner = game.play_hand()
        num_games += 1
        if winner is None:
            break
    print(f"number of games is: {num_games}")

        


if __name__ == "__main__":
    player1 = ConsolePlayer("player 1", 1000)
    player2 = RandomPlayer("player 2", 1000, )
    play_game(player1, player2)
