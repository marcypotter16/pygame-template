import time
from Generic.CyclicList import CyclicList
from Generic.Stack import Stack
from GraphicClasses import GraphicBot, GraphicCard, GraphicDeck, GraphicPlayer, GraphicBoard
from States.EndGame import EndGameState
from States.State import State
import pygame as p

from Utils.Text import draw_text
from Utils.Timer import Timer

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = GraphicPlayer(game)
        self.bot = GraphicBot(game, show_hand=False, smart=True)
        self.board = GraphicBoard(game)
        self.deck = GraphicDeck(game, size=40, position=(200, game.GAME_H // 2 - 75), card_dimensions=(100, 150))
        self.deck.shuffle()
        self.timer = Timer()
        self.turn_count: int = 0
        self.states = CyclicList()
        self.states.add("BeginTurn")
        for _ in range(3):
            self.states.add("PlayerTurn")
            self.states.add("BotTurn")
        self.states.set_current(0)
        self.last_to_take = "Bot"
        self.animating_last_turn = False

    def render(self, surface):
        super().render(surface)
        self.board.render(surface)
        self.deck.render(surface)
        self.bot.render(surface)
        self.player.render(surface)
        draw_text(self.game.font_medium, surface, f"Turno {self.turn_count // 2 + 1}", (255, 255, 255), 0, 0)

    def update(self, delta_time):
        super().update(delta_time)
        self.board.update()
        self.deck.update()
        if self.states.get_current() == "BeginTurn":
            if self.deck.is_empty():
                # Play the last animation and go to the end game state
                if not self.animating_last_turn:
                    # Who took last takes everything on the board
                    who_took_last = self.player if self.last_to_take == "Player" else self.bot
                    who_took_last.graphic_won_cards.add_cards(self.board.cards)
                    who_took_last.won_cards.extend(self.board.cards)
                    self.board.cards = []
                    who_took_last.graphic_won_cards.rearrange()
                    self.board.rearrange()
                    self.animating_last_turn = True
                if self.game.tweener.is_empty():
                    print([str(c) for c in self.player.won_cards], [str(c) for c in self.bot.won_cards])
                    EndGameState(self.game, [self.player, self.bot]).enter_state()
            else:
                self.player.draw_cards(self.deck, 3)
                self.bot.draw_cards(self.deck, 3)
                # Add 4 cards at the beginning of the game
                if self.turn_count == 0:
                    self.board.cards.extend([GraphicCard.from_card(c, self.game) for c in self.deck.draw(4)])
                self.board.rearrange()
                self.states.next()
        if self.states.get_current() == "PlayerTurn":
            self.update_player(delta_time)
        if self.states.get_current() == "BotTurn":
            self.update_bot(delta_time)

        self.bot.scope_text = f"Scope: {self.bot.scope}"
        self.player.scope_text = f"Scope: {self.player.scope}"

        self.last_to_take = "Bot" if self.bot.has_taken_last_turn else "Player"

    def update_player(self, delta_time):
        self.player.update()
        for card in self.player.graphic_hand.cards:
            if card.dropped:
                if self.board.rect.collidepoint(card.rect.center):
                    self.player.play_card(card, self.board)
                    self.turn_count += 1
                    self.states.next()
                else:
                    card.snap_back()

    def update_bot(self, delta_time):
        self.bot.update()
        if not self.bot.has_played_card:
            self.bot.play_card(self.bot.think(self.board), self.board, then=self.states.next)
            self.bot.has_played_card = True
            self.turn_count += 1
        # Wait for animations to finish
        # if len(self.game.tweener.tweens) == 0:
        #     self.turn_count += 1
        #     self.states.next()

