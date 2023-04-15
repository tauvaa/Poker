from src.frontend.displays.console import ConsoleDisplay
from src.player import Player
from src.utils.betting import BetOption, BettingDecision


class ConsolePlayer(Player):
    def __init__(self, player_name, bank, player_id=None):
        super().__init__(player_name, bank, player_id, display=ConsoleDisplay)

    def unpack_bet(self, bet_string):
        _, amount = bet_string.split(" ")
        amount = int(float(amount))
        if amount <= 0:
            raise ValueError("amount is not high enough")

        return amount

    def _decision(self, bet_amount, bet_options, game_info):
        options = ", ".join([x.name for x in bet_options])
        while True:
            decision_string = f"""you can {options}\n"""
            decision = input(decision_string)

            if decision == "call":
                return BettingDecision(BetOption.call, 0)

            elif decision == "check":
                return BettingDecision(BetOption.check, 0)

            elif decision == "fold":
                return BettingDecision(BetOption.fold, 0)
            elif decision.startswith("bet"):
                try:
                    amount = self.unpack_bet(decision)
                except Exception as err:
                    print("that was an invaild bet")
                else:
                    return BettingDecision(BetOption.bet, amount)
            else:
                print("you can't do that")
