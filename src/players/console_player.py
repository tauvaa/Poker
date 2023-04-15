from src.player import Player
from src.utils.betting import BetOption, BettingDecision
from src.frontend.displays.console import ConsoleDisplay


class ConsolePlayer(Player):
    def __init__(self, player_name, bank, player_id=None):
        super().__init__(player_name, bank, player_id, display=ConsoleDisplay)

    def _decision(self, bet_amount, bet_options, game_info):
        return BettingDecision(BetOption.check, 0)
