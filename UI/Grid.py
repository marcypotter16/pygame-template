from UI.Abstract import UIContainer
from Utils.Colors import WHITE


class UIGrid(UIContainer):
    def __init__(self, parent, x=0, y=0, center=None, width=100, height=100, bg_color=(40, 40, 40), fg_color=WHITE,
                 corner_radius=10, pad=(0, 0), font=None, rows=1, cols=1, border_width=0):
        super().__init__(parent, x, y, center, width, height, bg_color, fg_color, font, corner_radius, border_width)
        self.rows = rows
        self.cols = cols
        self.pad = pad
        # w = pad_x + (cell_w + pad_x) * cols => cell_w = (w - pad_x) // cols - pad_x
        self.cell_width = (width - pad[0]) // cols - pad[0]
        self.cell_height = (height - pad[1]) // rows - pad[1]

        self.cells: dict[tuple[int, int], UIContainer] = {} # (row, col) -> UIContainer

    def add_child(self, child, row, col):
        super().add_child(child)
        self.cells[(row, col)] = child
        child.rect.update(self.x + col * (self.cell_width + self.pad[0]) + self.pad[0],
                          self.y + row * (self.cell_height + self.pad[1]) + self.pad[1],
                          self.cell_width, self.cell_height)

    def recalculate_cell_dimensions(self):
        self.cell_width = (self.width - self.pad[0]) // self.cols - self.pad[0]
        self.cell_height = (self.height - self.pad[1]) // self.rows - self.pad[1]
        self.expand_to_fit_children()

    def expand_to_fit_children(self):
        self.width = self.cols * (self.cell_width + self.pad[0]) + self.pad[0]
        self.height = self.rows * (self.cell_height + self.pad[1]) + self.pad[1]

    def render(self, surface):
        super().render(surface)

    def clear(self):
        super().clear()
        self.cells.clear()
        print(f"Cleared grid: cells: {self.cells}, children: {self.children}")

    def update(self, dt):
        super().update(dt)