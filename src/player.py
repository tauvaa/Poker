import abc

from src.utils.hand import Hand


class Player:
    def __init__(self, player_name, bank, player_id=None):
        self.hand = Hand()
        self.player_name = player_name
        self.bank = bank
        self.player_id = player_id or player_name.lower().replace(" ", "_")

    def add_card(self, card):
        """Use to add card to player hand."""
        self.hand.add_card(card)

    def update_bank(self, amount):
        """Use to update player bank by amount."""
        self.bank += amount

    def decision(self, bet_amount, bet_options):
        """Use to make decision to check, call, bet, fold."""
        # TODO turn this into an abstact method.
        pass

    def __eq__(self, obj):
        if obj.player_id == self.player_id:
            return True
        return False
