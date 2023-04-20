from src.frontend.displays.gui.gui import GuiDisplay
from src.game import GamePhase, GameState
from src.player import Player
from src.utils.betting import BetOption, BettingDecision


class GuiPlayer(Player):
    def __init__(self, player_name, bank, player_id=None, display=None):
        super().__init__(player_name, bank, player_id, display=GuiDisplay)


    def decision(self, bet_amount, bet_options, game_info):
        if self.display:
            decision, amount = self.display.show(game_info)
            return BettingDecision(decision, amount)
