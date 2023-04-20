from src.player import Player
from src.utils.betting import BetOption, BettingDecision


class CheckCallPlayer(Player):
    def __init__(self, player_name, bank, player_id=None, display=None):
        super().__init__(player_name, bank, player_id, display)
        pass

    def decision(self, bet_amount, bet_options, game_info):
        if BetOption.call in bet_options:
            return BettingDecision(BetOption.call, 0)
        if BetOption.check in bet_options:
            return BettingDecision(BetOption.check, 0)
