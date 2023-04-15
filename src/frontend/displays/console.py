"""
Basic Console display, used mostly for dev/testing
"""
from src.frontend.display import Display
from src.game import GamePhase, GameState
from src.utils.betting import BetOption


class ConsoleDisplay(Display):
    def __init__(self):
        super().__init__()

    def show(self, game_info: GameState, *args, **kwargs):
        my_cards = ", ".join([str(x) for x in game_info.player.hand.cards])
        pot = game_info.pot
        winner_string = ""
        if game_info.game_phase == GamePhase.check_cards:
            if game_info.winner is not None:
                winner_info = self.hand_checker.get_hand(game_info.winner.hand)
                winner_string = f"""winner: {game_info.winner.player_name} {winner_info}\n"""
            else:
                winner_string = "game was a tie"
        show_string = f"""
{winner_string}{game_info.player.player_name}
has {my_cards}
the pot is at: {pot}
        """
        if game_info.bet_amount is not None and game_info.bet_amount > 0:
            show_string += f"\nit is {game_info.bet_amount} to call"

        print(show_string)
