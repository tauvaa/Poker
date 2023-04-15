import abc

from src.utils.hand import Hand


class Player:
    def __init__(self, player_name, bank, player_id=None, display=None):
        self.hand = Hand()
        self.player_name = player_name
        self.bank = bank
        self.player_id = player_id or player_name.lower().replace(" ", "_")
        self.display = None
        if display is not None:
            self.display = display()

    def add_card(self, card):
        """Use to add card to player hand."""
        self.hand.add_card(card)

    def update_bank(self, amount):
        """Use to update player bank by amount."""
        self.bank += amount

    def _decision(self, bet_amount, bet_options, game_info):
        """Use to make decision to check, call, bet, fold."""
        # TODO turn this into an abstact method.
        pass

    def decision(self, bet_amount, bet_options, game_info):
        if self.display is not None:
            self.display.show(game_info)
        return self._decision(bet_amount, bet_options, game_info)


    def __eq__(self, obj):
        if obj.player_id == self.player_id:
            return True
        return False
