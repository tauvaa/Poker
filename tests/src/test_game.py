import unittest
from unittest.mock import Mock, patch

from src.game import Game, GameState
from src.player import Player
from src.utils.betting import BetOption, BettingDecision
from src.utils.deck import Card, Suit


class TestGameStages(unittest.TestCase):
    def setUp(self):
        self.start_bank = 1000
        player1 = Player("Player 1", self.start_bank)
        player2 = Player("Player 2", self.start_bank)
        self.game = Game(player1, player2)

    def test_deal_card(self):
        self.game.deal_card(self.game.player1)
        self.assertEqual(len(self.game.deck.cards), 51)
        self.assertEqual(len(self.game.player1.hand.cards), 1)

    @patch("src.game.Game.betting")
    @patch("src.utils.deck.Deck.shuffle")
    def test_preflop(self, mock_deck, mock_betting):
        mock_betting.return_value = False
        outcome = self.game.preflop()
        self.assertFalse(outcome)
        self.assertEqual(
            self.game.pot.amount, self.game.small_blind + self.game.big_blind
        )
        self.assertEqual(
            self.game.player1.bank, self.start_bank - self.game.big_blind
        )
        self.assertEqual(
            self.game.player2.bank, self.start_bank - self.game.small_blind
        )
        self.assertEqual(len(self.game.player2.hand.cards), 2)
        self.assertEqual(len(self.game.player1.hand.cards), 2)
        mock_deck.assert_called_once()
        mock_betting.assert_called_once()

    @patch("src.game.Game.betting")
    def test_flop(self, mock_betting):
        mock_betting.return_value = False
        outcome = self.game.flop()
        self.assertFalse(outcome)
        self.assertEqual(len(self.game.player2.hand.cards), 3)
        self.assertEqual(len(self.game.player1.hand.cards), 3)
        self.assertEqual(len(self.game.community_cards), 3)
        self.assertEqual(mock_betting.call_count, 1)

    @patch("src.game.Game.betting")
    def test_turn(self, mock_betting):
        mock_betting.return_value = False
        outcome = self.game.turn()
        self.assertFalse(outcome)
        self.assertEqual(len(self.game.player2.hand.cards), 1)
        self.assertEqual(len(self.game.player1.hand.cards), 1)
        self.assertEqual(len(self.game.community_cards), 1)
        self.assertEqual(mock_betting.call_count, 1)

    @patch("src.game.Game.betting")
    def test_river(self, mock_betting):
        mock_betting.return_value = False
        outcome = self.game.turn()
        self.assertFalse(outcome)
        self.assertEqual(len(self.game.player2.hand.cards), 1)
        self.assertEqual(len(self.game.player1.hand.cards), 1)
        self.assertEqual(len(self.game.community_cards), 1)
        self.assertEqual(mock_betting.call_count, 1)

    def test_new_hand_winner(self):
        win_amount = 100
        self.game.winner = self.game.player2
        self.game.dealer = self.game.player2
        self.game.pot.amount = win_amount
        self.game.community_cards = [
            Card(10, Suit.heart.name),
            Card(11, Suit.club.name),
            Card(6, Suit.club.name),
        ]
        self.game.new_hand()
        self.assertEqual(self.game.player2.bank, self.start_bank + win_amount)
        self.assertEqual(self.game.pot.amount, 0)
        self.assertEqual(self.game.dealer, self.game.player1)
        self.assertListEqual(self.game.community_cards, [])
        self.assertListEqual(self.game.player1.hand.cards, [])
        self.assertListEqual(self.game.player2.hand.cards, [])
        self.assertEqual(self.game.game_state, GameState.preflop)

    def test_new_hand_no_winner(self):
        win_amount = 100
        self.game.dealer = self.game.player2
        self.game.pot.amount = win_amount
        self.game.community_cards = [
            Card(10, Suit.heart.name),
            Card(11, Suit.club.name),
            Card(6, Suit.club.name),
        ]
        self.game.new_hand()
        self.assertEqual(
            self.game.player2.bank, self.start_bank + win_amount / 2
        )
        self.assertEqual(
            self.game.player1.bank, self.start_bank + win_amount / 2
        )
        self.assertEqual(self.game.pot.amount, 0)
        self.assertListEqual(self.game.community_cards, [])
        self.assertListEqual(self.game.player1.hand.cards, [])
        self.assertListEqual(self.game.player2.hand.cards, [])
        self.assertEqual(self.game.game_state, GameState.preflop)


class TestGameBetting(unittest.TestCase):
    def setUp(self):
        self.start_bank = 1000
        player1 = Player("Player 1", self.start_bank)
        player2 = Player("Player 2", self.start_bank)
        self.game = Game(player1, player2)

    @patch("src.player.Player.decision")
    def test_betting_bet_fold(self, mock_player_decision):
        bet_amount = 100
        mock_player_decision.side_effect = [
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.bet, 0),
            BettingDecision(BetOption.fold, 0),
        ]
        betting_outcome = self.game.betting()
        self.assertEqual(self.game.player2.bank, self.start_bank - bet_amount)
        self.assertEqual(self.game.player1.bank, self.start_bank - bet_amount)
        self.assertFalse(betting_outcome)
        self.assertEqual(self.game.winner, self.game.player1)
        self.assertEqual(self.game.loser, self.game.player2)

    @patch("src.player.Player.decision")
    def test_betting_bet_call(self, mock_player_decision):
        bet_amount = 100
        mock_player_decision.side_effect = [
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.call, 0),
        ]
        betting_outcome = self.game.betting()
        self.assertEqual(self.game.player2.bank, self.start_bank - bet_amount)
        self.assertEqual(self.game.player1.bank, self.start_bank - bet_amount)
        self.assertEqual(self.game.pot.amount, 2 * bet_amount)
        self.assertTrue(betting_outcome)

    @patch("src.player.Player.decision")
    def test_betting_check_check(self, mock_player_decision):
        bet_amount = 100
        mock_player_decision.side_effect = [
            BettingDecision(BetOption.check, 0),
            BettingDecision(BetOption.check, 0),
        ]
        betting_outcome = self.game.betting()
        self.assertEqual(self.game.player2.bank, self.start_bank)
        self.assertEqual(self.game.player1.bank, self.start_bank)
        self.assertEqual(self.game.pot.amount, 0)
        self.assertTrue(betting_outcome)
        self.assertEqual(mock_player_decision.call_count, 2)

    @patch("src.player.Player.decision")
    def test_betting_check_bet_call(self, mock_player_decision):
        bet_amount = 100
        mock_player_decision.side_effect = [
            BettingDecision(BetOption.check, 0),
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.call, 0),
        ]
        betting_outcome = self.game.betting()
        self.assertEqual(self.game.player2.bank, self.start_bank - bet_amount)
        self.assertEqual(self.game.player1.bank, self.start_bank - bet_amount)
        self.assertEqual(self.game.pot.amount, 2 * bet_amount)
        self.assertTrue(betting_outcome)
        self.assertEqual(mock_player_decision.call_count, 3)

    @patch("src.player.Player.decision")
    def test_betting_check_bet_bet_call(self, mock_player_decision):
        bet_amount = 100
        mock_player_decision.side_effect = [
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.call, 0),
        ]
        betting_outcome = self.game.betting()
        self.assertEqual(
            self.game.player2.bank, self.start_bank - 2 * bet_amount
        )
        self.assertEqual(
            self.game.player1.bank, self.start_bank - 2 * bet_amount
        )
        self.assertEqual(self.game.pot.amount, 4 * bet_amount)
        self.assertTrue(betting_outcome)
        self.assertEqual(mock_player_decision.call_count, 3)


class TestPlayHand(unittest.TestCase):
    def setUp(self):
        self.start_bank = 1000
        player1 = Player("Player 1", self.start_bank)
        player2 = Player("Player 2", self.start_bank)
        self.game = Game(player1, player2)

    @patch("src.game.Game.new_hand")
    @patch("src.game.Game.preflop")
    def test_play_hand_preflop(self, mock_preflop, mock_new_hand):
        mock_preflop.return_value = False
        self.game.play_hand()
        self.assertEqual(mock_new_hand.call_count, 1)

    @patch("src.game.Game.new_hand")
    @patch("src.game.Game.betting")
    def test_play_hand_flop(self, mock_betting, mock_new_hand):
        mock_betting.side_effect = [True, False]
        self.game.play_hand()
        self.assertEqual(self.game.game_state, GameState.flop)
        self.assertEqual(mock_new_hand.call_count, 1)

    @patch("src.game.Game.new_hand")
    @patch("src.game.Game.betting")
    def test_play_hand_turn(self, mock_betting, mock_new_hand):
        mock_betting.side_effect = [True, True, False]
        self.game.play_hand()
        self.assertEqual(self.game.game_state, GameState.turn)
        self.assertEqual(mock_new_hand.call_count, 1)

    @patch("src.game.Game.new_hand")
    @patch("src.game.Game.betting")
    def test_play_hand_river(self, mock_betting, mock_new_hand):
        mock_betting.side_effect = [True, True, True, False]
        self.game.play_hand()
        self.assertEqual(self.game.game_state, GameState.river)
        self.assertEqual(mock_new_hand.call_count, 1)

    @patch("src.game.Game.new_hand")
    @patch("src.game.Game.betting")
    def test_play_hand_full(self, mock_betting, mock_new_hand):
        mock_betting.side_effect = [True, True, True, True]
        self.game.play_hand()
        self.assertEqual(self.game.game_state, GameState.river)
        self.assertEqual(mock_new_hand.call_count, 1)

    @patch("src.utils.deck.Deck.shuffle")
    @patch("src.game.Game.new_hand")
    @patch("src.player.Player.decision")
    def test_game_sim_1(self, mock_decision, mock_new_hand, mock_shuffle):
        """
        Simulate a full game, player 1 to have 2 pair (jacks, 10s) player 2 to
        have pair 3s.
        """
        bet_amount = 100
        preflop_decision = [
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.call, 0),
        ]
        # pot should be at 2 * bet amount
        flop_decision = [
            BettingDecision(BetOption.check, bet_amount),
            BettingDecision(BetOption.check, 0),
        ]

        turn_decision = [
            BettingDecision(BetOption.check, 0),
            BettingDecision(BetOption.bet, bet_amount),
            BettingDecision(BetOption.call, 0),
        ]
        # pot should be at 4 * bet amount (each player bank down 2*bet amount)

        river_decision = [
            BettingDecision(BetOption.check, bet_amount),
            BettingDecision(BetOption.check, 0),
        ]
        decisions = (
            preflop_decision + flop_decision + turn_decision + river_decision
        )
        mock_decision.side_effect = decisions

        preflop_cards = [
            Card(3, Suit.heart.name),
            Card(11, Suit.heart.name),
            Card(5, Suit.heart.name),
            Card(10, Suit.heart.name),
        ]
        burn_1 = [Card(14, Suit.diamond.name)]
        flop_cards = [
            Card(11, Suit.club.name),
            Card(10, Suit.spade.name),
            Card(3, Suit.diamond.name),
            # burn card
        ]
        burn_2 = [Card(14, Suit.club.name)]
        turn_cards = [
            Card(7, Suit.club.name),
        ]
        burn_3 = [Card(11, Suit.spade.name)]
        river_cards = [Card(14, Suit.spade.name)]
        cards = (
            preflop_cards
            + burn_1
            + flop_cards
            + burn_2
            + turn_cards
            + burn_3
            + river_cards
        )

        self.game.deck.cards = cards
        self.game.play_hand()
        self.assertTrue(
            self.game.player1.bank, 2 * bet_amount + self.start_bank
        )
        self.assertTrue(
            self.game.player2.bank, 2 * bet_amount - self.start_bank
        )
        self.assertEqual(self.game.player1, self.game.winner)
        mock_new_hand.assert_called_once()


if __name__ == "__main__":
    unittest.main()
