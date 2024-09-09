import pygame

from Game import Game
from Utils import Draw


class UICanvas:
    def __init__(self, game: Game):
        self.game = game
        self.font = game.font_medium
        self.y = None
        self.width = None
        self.x = None
        self.rect = None
        self.children: list[UIContainer] = []
        self.visible = True

    def render(self, surface: pygame.Surface):
        for child in self.children:
            child.render(surface)

    def update(self, dt):
        for ui_element in self.children:
            ui_element.update(dt)


class UIContainer(UICanvas):
    def __init__(self, parent: UICanvas, x=0, y=0, center: tuple[int, int] = None, width=100, height=100,
                 bg_color: tuple | str = (40, 40, 40), fg_color=(0, 0, 0), corner_radius=10):
        """
        Container for GUI
        :param parent: the parent, usually a UICanvas
        :param x: x of the center of the container
        :param y: y of the center of the container
        :param center: tuple containing the center of the container. If this is not none, this will overwrite x and y
        :param width: width of the container
        :param height: height of the container
        :param bg_color: background colour
        :param fg_color: foreground colour (text)
        :param corner_radius: corner radius for smoothed rectangles
        """
        self.x = x
        self.y = y
        if center is not None:
            self.x, self.y = center[0] - width / 2, center[1] - height / 2
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)
        if bg_color == "transparent":
            self.original_bg_color = self.bg_color = (0, 0, 0, 0)
        else:
            self.original_bg_color = self.bg_color = bg_color
        self.fg_color = fg_color
        self.corner_radius = corner_radius

        self.children: list[UIContainer] = []

        self.visible = True

        self.parent = parent
        self.game = self.parent.game
        self.font = self.game.font_medium

        self.parent.children.append(self)

    def rescale(self, rect: pygame.rect.Rect):
        px, py = self.x, self.y
        self.rect = rect
        horizontal_scaling_factor = float(rect.width) / self.width
        vertical_scaling_factor = float(rect.height) / self.height
        self.x, self.y, self.width, self.height = rect.x, rect.y, rect.width, rect.height
        for child in self.children:
            child.x = self.x + round(horizontal_scaling_factor * (child.x - px))
            child.y = self.y + round(vertical_scaling_factor * (child.y - py))
            child.height = round(child.height * vertical_scaling_factor)
            child.width = round(child.width * horizontal_scaling_factor)
            child.rect.update(child.x, child.y, child.width, child.height)

    def render(self, surface: pygame.Surface):
        # super().render(surface)
        # surface.fill(self.original_bg_color, self.rect)
        if self.visible:
            # pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.corner_radius)
            Draw.draw_rect_alpha(surface, color=self.bg_color, rect=self.rect)
        for child in self.children:
            child.render(surface)

    def update(self, dt):
        for ui_element in self.children:
            ui_element.update(dt)


class UIElement(UIContainer):
    def __init__(self, parent: UICanvas = None, x=0, y=0, center=None, width=100, height=100,
                 bg_color: tuple | str = (40, 40, 40),
                 fg_color=(0, 0, 0), text: str = "", corner_radius=10):
        super().__init__(parent, x, y, center, width, height, bg_color, fg_color, corner_radius)

        self.clickable: bool = False
        self.text = text

        self.game = self.parent.game

    def pack(self, side: str, padx: int = 0, pady: int = 0):
        """
        Makes the children fit nicely inside the parent. Width or Height might get modified to fit in the frame.
        :param side: vert or horiz
        :param padx: horizontal padding
        :param pady: vertical padding
        :return: None
        """

        # self.parent.width = max([child.width for child in self.parent.children]) + 2 * padx

        s = side.lower()
        if s == "vert":
            # Not very stonks
            self.parent.height = sum(child.height + pady for child in self.parent.children) + pady
            self.x = self.parent.x + padx
            self.width = self.parent.width - 2 * padx
            if len(self.parent.children) > 1:
                self.y = max(child.y for child in self.parent.children) + pady + self.height
            else:
                self.y = self.parent.y + pady

        elif s == "horiz":
            # Not very stonks
            self.parent.width = sum(child.width + padx for child in self.parent.children) + padx
            self.y = self.parent.y + pady
            self.height = self.parent.height - 2 * pady
            if len(self.parent.children) > 1:
                self.x = self.parent.children[0].x + padx + self.width
            else:
                self.x = self.parent.x + padx

        self.rect.update(self.x, self.y, self.width, self.height)
        self.parent.rect.update(self.parent.x, self.parent.y, self.parent.width, self.parent.height)

    def render(self, surface: pygame.Surface):
        super().render(surface)

    def update(self, dt):
        for ui_element in self.children:
            ui_element.update(dt)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.width}, {self.height}"
