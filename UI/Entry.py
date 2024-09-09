import pygame

from UI.Abstract import UIElement, UICanvas
from Utils.Text import draw_centered_text


class Entry(UIElement):
    def __init__(self, parent: UICanvas = None, x=0, y=0, center=None, width=100, height=100, bg_color: tuple | str = (50, 50, 50),
                 fg_color=(0, 0, 0), placeholder: str = "", corner_radius=10, focus_color=(150, 150, 150), is_password=False):

        super().__init__(parent, x, y, center, width, height, bg_color, fg_color, placeholder, corner_radius)
        self.focused = False
        self.focus_color = focus_color
        self.original_fg_color = fg_color
        self.is_password = is_password
        if is_password:
            self.text = ""

    def render(self, surface: pygame.Surface):
        if self.visible:
            super().render(surface)
            pygame.draw.rect(surface, self.fg_color, self.rect, width=3, border_radius=self.corner_radius)
            text = '*'*len(self.text) if self.is_password else self.text
            draw_centered_text(self.font, surface, text, self.fg_color, self.rect)

    def update(self, dt):
        if self.visible:
            if self.game.clicked_sx == -1:
                if self.rect.collidepoint(self.game.mousepos):
                    self.focused = True
                    self.fg_color = self.focus_color
                    self.game.need_key_event_handling = False
                else:
                    self.focused = False
                    self.fg_color = self.original_fg_color
                    self.game.need_key_event_handling = True

            if self.focused:
                for event in self.game.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            # Delete last character
                            self.text = self.text if self.text == "" else self.text[:-1]

                        elif event.unicode.isprintable():
                            if self.font.size(self.text)[0] <= self.width - 40:
                                self.text += event.unicode

