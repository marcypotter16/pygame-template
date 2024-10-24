from functools import partial
from random import random
import pygame
from pygame.draw import circle
from pygame import Vector2
from States.State import State
from UI.Button import TextButton
from UI.Containers import VertContainer
from UI.Entry import Paragraph
from UI.Grid import UIGrid
from UI.Label import Label
from math import sin
from time import time

from Utils.Colors import *
from ui_custom import CellInputInterface


class BlankState(State):
    def __init__(self, game, msg=None, layer="foreground"):
        super().__init__(game, msg, layer)

        # Create a label, it parents itself to self.canvas (inherited from State)
        self.label = Label(self.canvas, center=self.game.SCREEN_CENTER,
                           text="Hi!", width=100, height=50, fg_color=(255, 255, 255))

        self.ci = CellInputInterface(self.game, pygame.Rect(300, 30, 400, 300))
        self.grid = UIGrid(self.canvas,
                           500,
                           500,
                            width=100,
                            height=100,
                            rows=3,
                            cols=3,
                            pad=(10, 10),
                            bg_color=BLACK,
                            fg_color=WHITE,
                            corner_radius=10,
                            border_width=5)
        # Populate the grid with labels
        for i in range(3):
            for j in range(3):
                self.grid.add_child(TextButton(self.canvas,
                                          text=f"{i}, {j}",
                                          fg_color=WHITE,
                                          font=self.game.font_small,
                                          command=lambda: print(i, j)), i, j)
                
        self.container = VertContainer(self.canvas,
                                       10,
                                       500,
                                       width=100,
                                       height=100,
                                       bg_color=BLACK,
                                       fg_color=WHITE,
                                       corner_radius=0)
        # Populate the container with text buttons
        for i in range(3):
            tb = TextButton(self.canvas,
                            text=f"Button {i}",
                            fg_color=WHITE,
                            font=self.game.font_small,
                            )
            tb.index = i
            tb.command = lambda j=i: print(j)
            self.container.add_child(tb)

        # def print_index(btn):
        #     print(btn.index)
        
        # for child in self.container.children:
        #     print(child.index)
        #     prt_ind = partial(print_index, child)
        #     child.command = prt_ind
        
        # Create a circle
        self.circle = Circle(self.game)

    def render(self, surface):
        super().render(surface)

        # Render the circle, the label is automatically rendered by the canvas
        self.circle.render(surface)

        self.ci.render(surface)

    def update(self, delta_time):
        super().update(delta_time)

        # Update the circle, the label is automatically updated by the canvas
        self.circle.update(delta_time)

        self.ci.update(delta_time)

        # Move the label with sine wave
        self.label.rect.y = self.game.SCREEN_CENTER[1] + 5 * sin(time() * 2)


class Circle:
    def __init__(self, game, radius=10):
        self.game = game
        self.velocity = Vector2(random(), random())
        self.velocity.normalize_ip()
        self.speed_mag = random() * 300
        self.position = Vector2(100, 100)
        self.radius = radius

    def render(self, surface):
        circle(surface, color=(255, 255, 255),
               center=self.position, radius=self.radius)

    def update(self, delta_time):
        self.position += self.velocity * self.speed_mag * delta_time
        if self.position.x < 0 or self.position.x > self.game.GAME_W:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > self.game.GAME_H:
            self.velocity.y *= -1
