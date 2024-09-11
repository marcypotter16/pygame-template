import pygame

from UI.Abstract import UIElement, UICanvas
from Utils.Text import draw_centered_text


class Label(UIElement):
    def __init__(self, parent: UICanvas = None, x=0, y=0, center=None, width=100, height=100,
                 font: pygame.font.Font = None, bg_color: tuple | str = (50, 50, 50),
                 fg_color=(0, 0, 0), text: str = "", corner_radius=10):
        super().__init__(parent, x, y, center, width, height,
                         bg_color, fg_color, text, corner_radius)

        if font is None:
            font = self.game.font_small
        else:
            self.font = font

    def render(self, surface: pygame.Surface):
        draw_centered_text(self.font, surface,
                           self.text, self.fg_color, self.rect)
