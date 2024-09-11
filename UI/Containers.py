from UI.Abstract import UIContainer, UICanvas, UIElement
from Utils.Text import draw_centered_text


# Abstract Container class
class VertContainer(UIContainer):
    def __init__(
        self,
        parent: UICanvas,
        x=0,
        y=0,
        center: tuple[int, int] = None,
        width=100,
        height=100,
        bg_color: tuple | str = ...,
        fg_color=...,
        corner_radius=10,
    ):
        super().__init__(
            parent, x, y, center, width, height, bg_color, fg_color, corner_radius
        )

    def add_child(self, child: UIElement):
        self.children.append(child)
        child.parent = self
        child.pack(side="vert")
