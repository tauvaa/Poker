import random

from src.frontend.displays.console import ConsoleDisplay
from src.player import Player
from src.utils.betting import BetOption, BettingDecision


class RandomPlayer(Player):
    def __init__(self, player_name, bank, player_id=None, display=None):
        super().__init__(player_name, bank, player_id, display=display)

    def _decision(self, bet_amount, bet_options, game_info, *args, **kwargs):

        random_choice = random.choice(bet_options)
        if random_choice == BetOption.check:
            print(f"{self.player_name} checks")
            return BettingDecision(BetOption.check, 0)
        if random_choice == BetOption.call:
            print(f"{self.player_name} calls")
            return BettingDecision(BetOption.call, 0)
        if random_choice == BetOption.fold:
            print(f"{self.player_name} folds")
            return BettingDecision(BetOption.fold, 0)
        if random_choice == BetOption.bet:
            print(f"{self.player_name} bets")
            return BettingDecision(BetOption.bet, 100)
