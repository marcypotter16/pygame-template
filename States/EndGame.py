from ConsoleGame import Deck
from Game import Game
from GraphicClasses import GraphicCard
from Player import PRIMIERA_VALUES, Bot, Player
from States.State import State
from Utils.Text import draw_centered_text, draw_text
import pygame as p


class EndGameState(State):
    def __init__(self, game, players: list[Player]):
        """
        Initializes the EndGameState object.

        Args:
            game (Game): The game object.
            players (list[Player]): The list of players, first is the player, second is the bot.
        """
        self.b_score = None
        self.p_score = None
        self.players = players
        self.player, self.bot = players
        self.player_cards = [GraphicCard.from_card(c, game) for c in self.player.won_cards]
        self.bot_cards = [GraphicCard.from_card(c, game) for c in self.bot.won_cards]
        self.p_diamond_cards = [GraphicCard.from_card(c, game) for c in self.get_diamonds(self.player_cards)]
        self.b_diamond_cards = [GraphicCard.from_card(c, game) for c in self.get_diamonds(self.bot_cards)]
        self.p_settebello = GraphicCard.from_card(self.get_settebello(self.player_cards), game)
        self.b_settebello = GraphicCard.from_card(self.get_settebello(self.bot_cards), game)
        self.p_primiera, self.p_primiera_score = [GraphicCard.from_card(c, game) for c in
                                                  self.get_primiera(self.player_cards)[0]], \
        self.get_primiera(self.player_cards)[1]
        self.b_primiera, self.b_primiera_score = [GraphicCard.from_card(c, game) for c in
                                                  self.get_primiera(self.bot_cards)[0]], \
        self.get_primiera(self.bot_cards)[1]
        super().__init__(game)
        self.rearrange_cards()
        self.get_total_scores()
        self.all_cards = self.player_cards.copy()
        self.all_cards.extend(self.bot_cards)
        self.all_cards.extend(self.p_diamond_cards)
        self.all_cards.extend(self.b_diamond_cards)
        if self.p_settebello:
            self.all_cards.append(self.p_settebello)
        if self.b_settebello:
            self.all_cards.append(self.b_settebello)
        self.all_cards.extend(self.p_primiera)
        self.all_cards.extend(self.b_primiera)

    def get_diamonds(self, cards: list) -> list[GraphicCard]:
        """
        Returns the list of cards that are diamonds.

        Args:
            cards (list): The list of cards.

        Returns:
            list[GraphicCard]: The list of cards that are diamonds.

        """
        return [c for c in cards if c.seme == "Q"]

    def get_settebello(self, cards: list) -> GraphicCard | None:
        """
        Returns the settebello card.

        Args:
            cards (list): The list of cards.

        Returns:
            GraphicCard: The settebello card or None if it doesn't exist.

        """
        if "7Q" in [str(c) for c in cards]:
            return [c for c in cards if str(c) == "7Q"][0]
        return None

    def get_primiera(self, cards: list) -> tuple[list[GraphicCard], int]:
        """
        Returns the best primiera cards and the sum of the score.

        Args:
            cards (list): The list of cards.

        Returns:
            tuple(list[GraphicCard], int): The best primiera cards and the sum of the score

        """
        best_cards = []
        for suit in ["P", "C", "Q", "F"]:
            l = sorted([c for c in cards if c.seme == suit], key=lambda c: PRIMIERA_VALUES[c.valore], reverse=True)
            if len(l) > 0:
                best_cards.append(l[0])
        return best_cards, sum([PRIMIERA_VALUES[c.valore] for c in best_cards])

    def get_total_scores(self):
        self.p_score = self.b_score = 0
        if len(self.player_cards) > 20:
            self.p_score += 1
        elif len(self.player_cards) < 20:
            self.b_score += 1
        if len(self.p_diamond_cards) > 5:
            self.p_score += 1
        elif len(self.p_diamond_cards) < 5:
            self.b_score += 1
        if self.p_primiera_score > self.b_primiera_score:
            self.p_score += 1
        elif self.p_primiera_score < self.b_primiera_score:
            self.b_score += 1
        if self.p_settebello:
            self.p_score += 1
        else:
            self.b_score += 1
        if {'JQ', 'QQ', 'KQ'} <= set([str(c) for c in self.player_cards]):
            self.p_score += 5
        elif {'JQ', 'QQ', 'KQ'} <= set([str(c) for c in self.bot_cards]):
            self.b_score += 5
        if {'AQ', '2Q', '3Q'} <= set([str(c) for c in self.player_cards]):
            self.p_score += 3
            for i in range(4, 7):
                if {f"{i}Q"} <= set([str(c) for c in self.player_cards]):
                    self.p_score += 1
                else:
                    break
        if {'AQ', '2Q', '3Q'} <= set([str(c) for c in self.bot_cards]):
            self.b_score += 3
            for i in range(4, 7):
                if {f"{i}Q"} <= set([str(c) for c in self.bot_cards]):
                    self.b_score += 1
                else:
                    break
        self.p_score += self.player.scope
        self.b_score += self.bot.scope

    def rearrange_cards(self):
        y_offset = 60
        x_offset = 20
        player_cards_topleft = (x_offset, y_offset)
        bot_cards_topleft = (x_offset + self.game.GAME_W // 2, y_offset)
        for i, c in enumerate(self.player_cards):
            c.move(player_cards_topleft[0] + i * 4, player_cards_topleft[1])
        for i, c in enumerate(self.bot_cards):
            c.move(bot_cards_topleft[0] + i * 4, bot_cards_topleft[1])
        # Denari
        y_offset = 220
        player_cards_topleft = (x_offset, y_offset)
        bot_cards_topleft = (x_offset + self.game.GAME_W // 2, y_offset)
        for i, c in enumerate(self.p_diamond_cards):
            c.move(player_cards_topleft[0] + i * c.width, player_cards_topleft[1])
        for i, c in enumerate(self.b_diamond_cards):
            c.move(bot_cards_topleft[0] + i * c.width, bot_cards_topleft[1])
        # Settebello
        y_offset = 370
        player_cards_topleft = (x_offset, y_offset)
        bot_cards_topleft = (x_offset + self.game.GAME_W // 2, y_offset)
        if self.p_settebello is not None:
            self.p_settebello.move(*player_cards_topleft)
        if self.b_settebello is not None:
            self.b_settebello.move(*bot_cards_topleft)
        # Primiera
        y_offset = 520
        player_cards_topleft = (x_offset, y_offset)
        bot_cards_topleft = (x_offset + self.game.GAME_W // 2, y_offset)
        for i, c in enumerate(self.p_primiera):
            c.move(player_cards_topleft[0] + i * c.width, player_cards_topleft[1])
        for i, c in enumerate(self.b_primiera):
            c.move(bot_cards_topleft[0] + i * c.width, bot_cards_topleft[1])

    def render(self, surface):
        """
        Renders the EndGameState.

        Args:
            surface (pygame.Surface): The surface to render on.

        """
        super().render(surface)
        p.draw.line(surface, (255, 255, 255), (self.game.GAME_W // 2, 0), (self.game.GAME_W // 2, self.game.GAME_H),
                    width=1)
        x_offset = 20
        y_off = 20
        draw_text(self.game.font_medium, surface, "Carte", (255, 255, 255), x_offset, y_off)
        draw_text(self.game.font_medium, surface, f"{len(self.player_cards)}", (255, 255, 255), x_offset + 400, y_off)
        draw_text(self.game.font_medium, surface, f"{len(self.bot_cards)}", (255, 255, 255),
                  x_offset + self.game.GAME_W // 2 + 400, y_off)
        for c in self.all_cards:
            c.render(surface)
        y_off = 180
        draw_text(self.game.font_medium, surface, "Denari", (255, 255, 255), x_offset, y_off)

        y_off = 330
        draw_text(self.game.font_medium, surface, "Settebello", (255, 255, 255), x_offset, y_off)

        y_off = 480
        draw_text(self.game.font_medium, surface, "Primiera", (255, 255, 255), x_offset, y_off)
        draw_text(self.game.font_big, surface, f"{self.p_primiera_score}", (255, 255, 255), x_offset + 400, y_off + 50)
        draw_text(self.game.font_big, surface, f"{self.b_primiera_score}", (255, 255, 255), x_offset + 1000, y_off + 50)

        y_off = 630
        draw_text(self.game.font_medium, surface, f"Scope: {self.player.scope}", (255, 255, 255), x_offset, y_off)
        draw_text(self.game.font_medium, surface, f"{self.bot.scope}", (255, 255, 255), x_offset + self.game.GAME_W // 2, y_off)

        draw_centered_text(self.game.font_big, surface, f"{self.p_score} - {self.b_score}", (255, 0, 0),
                           p.Rect((0, 0), (self.game.GAME_W, self.game.GAME_H)))


if __name__ == "__main__":
    g = Game()
    pl = Player()
    b = Bot()
    d = Deck()
    d.shuffle()
    pl.won_cards = d.draw(20)
    b.won_cards = d.draw(20)
    egs = EndGameState(g, [pl, b])
    print([str(c) for c in egs.get_primiera(pl.won_cards)[0]], egs.get_primiera(pl.won_cards)[1])
