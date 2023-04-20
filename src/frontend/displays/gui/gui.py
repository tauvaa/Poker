import os

import pygame
from src.frontend.display import Display
from src.frontend.displays.config import (HEIGHT, IMAGEFOLDER, SCREENSIZE,
                                          SQUARESIZE, WIDTH)
from src.game import GamePhase, GameState
from src.utils.betting import BetOption


class PotDisplay:
    def __init__(self, amount, position, banner):
        self.x, self.y = position
        self.height, self.width = 2 * SQUARESIZE, 3 * SQUARESIZE
        self.amount = amount
        self.banner = banner

    def draw(self, screen):
        pygame.draw.rect(
            screen, "grey", (self.x, self.y, self.width, self.height)
        )
        font = pygame.font.SysFont("Arial", 20)
        amount = font.render(str(self.amount), True, (0, 0, 0))
        banner = font.render(self.banner, True, (0, 0, 0))
        screen.blit(amount, (self.x, self.y + SQUARESIZE))
        screen.blit(banner, (self.x, self.y))


class CardDisplay:
    def __init__(self, card, position, show_card=True):
        self.card = card
        self.x, self.y = position
        self.height, self.width = 3 * SQUARESIZE, 2 * SQUARESIZE
        self.show_card = show_card

    def draw(self, screen):
        font = pygame.font.SysFont("arial", 20)
        pygame.draw.rect(
            screen, "purple", (self.x, self.y, self.width, self.height)
        )

        card_suit = self.card.suit
        if card_suit == "club":
            file = "club.png"
        if card_suit == "spade":
            file = "spade.png"
        if card_suit == "heart":
            file = "heart.png"
        if card_suit == "diamond":
            file = "diamond.png"

        card_value = str(self.card.value)
        if card_value == "11":
            card_value = "Jack"
        if card_value == "12":
            card_value = "Queen"
        if card_value == "13":
            card_value = "King"
        if card_value == "14":
            card_value = "Ace"
        if self.show_card:
            value = font.render(card_value, True, (0, 0, 0))
            suit = pygame.image.load(os.path.join(IMAGEFOLDER, file))
            screen.blit(suit, (self.x, self.y))
            screen.blit(value, (self.x, self.y + self.height - SQUARESIZE))


class GuiDisplay(Display):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()
        self.bet_button = None
        self.call_button = None
        self.fold_button = None
        self.display_cards = []
        self.display_objects = []
        self.display_type = "game"
        self.winner_string = None

    def reset_game(self):
        print("resetting")
        self.display_objects = []
        self.display_cards = []
        self.display_type = "game"
        self.winner_string = None

    def decision_options(self, bet_options):
        """Use to draw the player options."""
        if bet_options is None:
            return

        font = pygame.font.SysFont("arial", 30)
        check_call = None

        if BetOption.call in bet_options:
            check_call = "Call"
        if BetOption.check in bet_options:
            check_call = "Check"

        self.bet_button = pygame.draw.rect(
            self.screen,
            "grey",
            (
                3 * SQUARESIZE,
                HEIGHT - SQUARESIZE,
                3 * SQUARESIZE,
                SQUARESIZE,
            ),
        )

        bet = font.render("bet", True, (0, 0, 0))
        BUTTONWIDTH = 3
        BUTTONSPACEWIDTH = 1
        self.screen.blit(
            bet,
            (BUTTONWIDTH * SQUARESIZE, HEIGHT - SQUARESIZE),
        )

        self.call_button = pygame.draw.rect(
            self.screen,
            "grey",
            (
                (2 * BUTTONWIDTH + BUTTONSPACEWIDTH) * SQUARESIZE,
                HEIGHT - SQUARESIZE,
                BUTTONWIDTH * SQUARESIZE,
                SQUARESIZE,
            ),
        )

        if check_call is not None:
            check_call = font.render(check_call, True, (0, 0, 0))
            self.screen.blit(
                check_call,
                dest=(
                    (2 * BUTTONWIDTH + BUTTONSPACEWIDTH) * SQUARESIZE,
                    HEIGHT - SQUARESIZE,
                ),
            )

        self.fold_button = pygame.draw.rect(
            self.screen,
            "grey",
            (
                (3 * BUTTONWIDTH + 2 * BUTTONSPACEWIDTH) * SQUARESIZE,
                HEIGHT - SQUARESIZE,
                BUTTONWIDTH * SQUARESIZE,
                SQUARESIZE,
            ),
        )

        fold = font.render("fold", True, (0, 0, 0))

        self.screen.blit(
            fold,
            (
                (3 * BUTTONWIDTH + 2 * BUTTONSPACEWIDTH) * SQUARESIZE,
                HEIGHT - SQUARESIZE,
            ),
        )

    def add_player_pots(self, game_state: GameState):
        self.display_objects.append(
            PotDisplay(
                game_state.player.bank,
                (10 * SQUARESIZE, HEIGHT - 4 * SQUARESIZE),
                game_state.player.player_name + " bank",
            )
        )
        self.display_objects.append(
            PotDisplay(
                game_state.opponent.bank,
                (10 * SQUARESIZE, HEIGHT - int(11.5 * SQUARESIZE)),
                game_state.opponent.player_name + " bank",
            )
        )

    def add_game_pot(self, game_state: GameState):
        self.display_objects.append(
            PotDisplay(
                game_state.pot,
                (4 * SQUARESIZE, HEIGHT - int(11.5 * SQUARESIZE)),
                "Game Pot",
            )
        )

    def add_community_cards(self, community_cards):
        cardx = 3 * SQUARESIZE
        for card in community_cards:
            self.display_cards.append(
                CardDisplay(card, (cardx, HEIGHT - (4 + 3 + 2) * SQUARESIZE))
            )
            cardx += 3 * SQUARESIZE

    def add_player_cards(self, player_cards):
        cardx = 2 * SQUARESIZE
        cardy = HEIGHT - (2 + 3) * SQUARESIZE  # * SQUARESIZE
        for card in player_cards:
            self.display_cards.append(CardDisplay(card, (cardx, cardy)))
            cardx += 3 * SQUARESIZE

    def add_opponent_cards(self, game_state: GameState):
        show_cards = (
            True if game_state.game_phase == GamePhase.check_cards else False
        )
        cardx = 2 * SQUARESIZE
        cardy = HEIGHT - 15 * SQUARESIZE  # * SQUARESIZE
        cards = game_state.opponent.hand.cards[0:2]
        for card in cards:
            self.display_cards.append(
                CardDisplay(card, (cardx, cardy), show_cards)
            )
            cardx += 3 * SQUARESIZE

    def winner(self, game_info):
        font = pygame.font.SysFont("Arial", 20)

        winner_string = "tie game with {}".format(
            self.hand_checker.get_hand(game_info.player.hand)["hand_type"]
        )
        if game_info.winner is not None:
            winning_hand = self.hand_checker.get_hand(game_info.winner.hand)
            winner_string = f"{game_info.winner.player_name} won with {winning_hand['hand_type']}"
        winner_string = font.render(winner_string, True, (0, 0, 0))
        self.winner_string = winner_string
        self.display_type = "winner_show"

    def show(self, game_info: GameState, *args, **kwargs):
        player_cards = game_info.player.hand.cards[0:2]
        self.add_player_cards(player_cards)
        self.add_community_cards(game_info.community_cards)
        self.add_player_pots(game_info)
        self.add_game_pot(game_info)
        self.add_opponent_cards(game_info)
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.display_type)
                    if self.display_type == "winner_show":
                        self.reset_game()
                        running = False
                        continue
                    if self.display_type == "winner":
                        self.display_type = "winner_show"
                        self.winner(game_info)
                        continue
                    if self.display_type == "fold":
                        self.reset_game()
                        running = False
                    point = pygame.mouse.get_pos()
                    if self.bet_button:
                        if self.bet_button.collidepoint(point):
                            return BetOption.bet, 100

                    if self.call_button:
                        if self.call_button.collidepoint(point):
                            if game_info.bet_options is not None:
                                if BetOption.call in game_info.bet_options:
                                    return BetOption.call, 0
                                else:
                                    return BetOption.check, 0
                    if self.fold_button is not None:
                        if self.fold_button.collidepoint(point):
                            return BetOption.fold, 0

            self.screen.fill("blue")

            for card in self.display_cards:
                card.draw(self.screen)
            for ojt in self.display_objects:
                ojt.draw(self.screen)

            self.decision_options(game_info.bet_options)
            if self.winner_string:
                self.screen.blit(
                    self.winner_string, (10 * SQUARESIZE, 10 * SQUARESIZE)
                )

            pygame.display.flip()
            if running:

                if (
                    GamePhase.check_cards == game_info.game_phase
                    and self.display_type != "winner"
                    and self.display_type != "winner_show"
                ):
                    self.display_type = "winner"
                elif game_info.winner is not None:
                    self.display_type = "fold"
