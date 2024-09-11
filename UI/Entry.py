import pygame

from UI.Abstract import UIElement, UICanvas
from Utils.Text import draw_centered_text
from Utils.Timer import Timer, SpacedCallback

from Game import Game

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
        self.key_pressed_timer = Timer()
        self.placeholder = placeholder

        self.key_pressed = None
        self.enter_key_callback = None

        self.caret = Caret(self.game, self)

    def render(self, surface: pygame.Surface):
        if self.visible:
            super().render(surface)
            pygame.draw.rect(surface, self.fg_color, self.rect, width=3, border_radius=self.corner_radius)
            text = '*'*len(self.text) if self.is_password else self.text
            draw_centered_text(self.font, surface, text, self.fg_color, self.rect)
            
            # Render caret
            self.caret.render(surface)

    def update(self, dt):
        if self.visible:
            
            # Update caret
            self.caret.update(dt)

            if self.key_pressed:
                self.key_pressed_timer.start(0.5)
                if self.key_pressed_timer.finished:
                    if self.key_pressed == pygame.K_BACKSPACE:
                        self._handle_backspace()
                    elif self.key_pressed == pygame.K_LEFT:
                        self._handle_arrow_left()
                    elif self.key_pressed == pygame.K_RIGHT:
                        self._handle_arrow_right()
                    elif self.key_pressed.isprintable():
                        self._handle_printable(self.key_pressed)
                self.key_pressed_timer.update(dt)

            if self.game.clicked_sx == -1:
                if self.rect.collidepoint(self.game.mousepos):
                    self.focused = True
                    self.fg_color = self.focus_color
                    self.game.need_key_event_handling = False

                    # Clear placeholder
                    if self.text == self.placeholder:
                        self.text = ""
                        self.caret.reset_position()
                else:
                    self.focused = False
                    self.fg_color = self.original_fg_color
                    self.game.need_key_event_handling = True
                    
                    # Restore placeholder
                    if self.text == "":
                        self.text = self.placeholder
                        self.caret.reset_position()

            if self.focused:
                for event in self.game.events:
                    if event.type == pygame.KEYDOWN:    

                        if event.mod & pygame.KMOD_CTRL:
                            if event.key == pygame.K_BACKSPACE:
                                if self.caret.index_in_text == 0:
                                    return
                                if self.text[self.caret.index_in_text - 1] == " ":
                                    self._handle_backspace()
                                    return
                                while self.caret.index_in_text > 0 and self.text[self.caret.index_in_text - 1] != " ":
                                    self._handle_backspace()

                            if event.key == pygame.K_DELETE:
                                if self.caret.index_in_text == len(self.text):
                                    return
                                if self.text[self.caret.index_in_text] == " ":
                                    self._hande_delete()
                                    return
                                while self.caret.index_in_text < len(self.text) and self.text[self.caret.index_in_text] != " ":
                                    self._hande_delete()

                        else:
                            if event.key == pygame.K_BACKSPACE:
                                # Delete character at the caret position
                                self._handle_backspace()

                            if event.key == pygame.K_DELETE:
                                # Delete character after the caret position
                                self._hande_delete()

                            elif event.key == pygame.K_LEFT:
                                self._handle_arrow_left()

                            elif event.key == pygame.K_RIGHT:
                                self._handle_arrow_right()

                            elif event.key == pygame.K_RETURN and self.enter_key_callback:
                                self.enter_key_callback()

                            elif event.unicode.isprintable():
                                self._handle_printable(event.unicode)

                        

                    
                    if event.type == pygame.KEYUP:
                        self.key_pressed = None
                        self.key_pressed_timer.stop()

    def set_enter_key_callback(self, callback):
        self.enter_key_callback = callback

    def _handle_backspace(self):
        if self.caret.index_in_text == 0:
            return
        self.caret.remove_char(self.text[self.caret.index_in_text - 1])
        aux_text = list(self.text)
        aux_text.pop(self.caret.index_in_text)
        aux_text = "".join(aux_text)
        self.text = self.text if self.text == "" else aux_text
        self.key_pressed = pygame.K_BACKSPACE

    def _hande_delete(self):
        if self.caret.index_in_text == len(self.text):
            return
        self.caret.delete_char(self.text[self.caret.index_in_text])
        aux_text = list(self.text)
        aux_text.pop(self.caret.index_in_text)
        aux_text = "".join(aux_text)
        self.text = self.text if self.text == "" else aux_text
        self.key_pressed = pygame.K_DELETE
    
    def _handle_printable(self, char):
        if self.font.size(self.text)[0] <= self.width - 40:
            aux_text = list(self.text)
            aux_text.insert(self.caret.index_in_text, char)
            self.text = "".join(aux_text)
            self.caret.add_char(char)
            self.key_pressed = char
    
    def _handle_arrow_left(self):
        if self.caret.index_in_text == 0:
            return
        self.caret.shift_char_left(self.text[self.caret.index_in_text - 1])
        self.key_pressed = pygame.K_LEFT

    def _handle_arrow_right(self):
        if self.caret.index_in_text == len(self.text):
            return
        self.caret.shift_char_right(self.text[self.caret.index_in_text])
        self.key_pressed = pygame.K_RIGHT

### --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Caret:
    def __init__(self, game: Game, parent: Entry):
        self.game = game
        self.parent = parent
        self.reset_position()
        self.timer = Timer()
        self.visible = True
        
        self.CARET_BLINK_SPEED = 0.4
        self.blink = SpacedCallback(self.toggle_visibility, 0.5)
        self.blink.start()

        self.color = (230, 230, 230)

        self.hiding = False

        ### abc|defg <- index_in_text = 3
        ### |abcdefg <- index_in_text = 0
        ### abcdefg| <- index_in_text = 7 = len(text)
        ### Removing a character from the text will move the caret to the left:
        ### abc|defg <- index_in_text = 2
        ### ab|defg <- index_in_text = 1

    def reset_position(self):
        self.offset = pygame.Vector2((self.parent.rect.width * .5 + self.parent.font.size(self.parent.text)[0] * .5, (self.parent.rect.height - self.parent.font.get_height()) // 2 - 3))
        self.topleft: pygame.Vector2 = self.parent.rect.topleft + self.offset
        self.rect = pygame.Rect(self.topleft, (2, self.parent.font.get_height() + 6))
        self.index_in_text = len(self.parent.text)
        print("Caret position RESET:", self.topleft, self.index_in_text)

    def add_char(self, char):
        self.topleft += pygame.Vector2(self.parent.font.size(char)[0] * .5, 0)
        self.rect.topleft = self.topleft
        self.index_in_text += 1

    def remove_char(self, char):
        self.topleft -= pygame.Vector2(self.parent.font.size(char)[0] * .5, 0)
        self.rect.topleft = self.topleft
        self.index_in_text -= 1

    def delete_char(self, char):
        # We don't need to move the caret to the left because the character after the caret will be deleted
        self.topleft += pygame.Vector2(self.parent.font.size(char)[0] * 0.5, 0)
        self.rect.topleft = self.topleft

    def shift_char_right(self, char):
        self.topleft += pygame.Vector2(self.parent.font.size(char)[0], 0)
        self.rect.topleft = self.topleft
        self.index_in_text += 1

    def shift_char_left(self, char):
        self.topleft -= pygame.Vector2(self.parent.font.size(char)[0], 0)
        self.rect.topleft = self.topleft
        self.index_in_text -= 1

    def hide(self):
        self.visible = False
        self.hiding = True

    def update(self, dt):
        if not self.hiding:
            self.blink.update(dt)
            # print("Caret position:", self.topleft, self.index_in_text)

    def render(self, surface: pygame.Surface):
        if self.visible and self.parent.focused:
            # pygame.draw.rect(surface, self.parent.fg_color, self.rect, width=3)
            pygame.draw.rect(surface, self.color, self.rect, width=3)

    def toggle_visibility(self):
        self.visible = not self.visible

