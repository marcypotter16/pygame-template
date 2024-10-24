from functools import partial
import sqlite3 as sql

from pygame import Color, PixelArray
import pygame
from States.State import State
from States.AddFreezerDialogState import AddFreezerDialogState
from States.AddBoxDialogState import AddBoxDialogState
from UI.Entry import Entry
from UI.Grid import UIGrid
from UI.Label import Label
from UI.Containers import VertContainer
from UI.Button import ImageButton, TextButton
from Utils.Colors import *

from pygame.image import load
from pygame.transform import smoothscale

from models import Cella, Freezer
from ui_custom import CellInputInterface


def change_black_to_white(img):
    # Convert the image to a format that allows pixel manipulation
    img = img.convert_alpha()

    # Get the pixel array
    pixel_array = PixelArray(img)

    # Iterate over each pixel and change black to white
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            # Check if the pixel is black
            if img.unmap_rgb(pixel_array[x, y])[:3] == (0, 0, 0):
                pixel_array[x, y] = Color(
                    255, 255, 255, 255)  # Change to white

    # Convert the pixel array back to a surface
    img = pixel_array.make_surface()

    # Clean up the pixel array
    del pixel_array

    return img


class AppState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.con = None
        self.cur = None
        self.init()

        self.bg_color = BACKGROUND

        self.freezers: dict[int, Freezer] = {}
        self.currently_opened_freezer = None
        self.currently_opened_box = None
        self.currently_selected_cell = None
        self.ci: CellInputInterface = None
        self.box_grid = None

        PANELS_OFFSET_Y = 100
        PANELS_Y = 120
        PANEL_HEIGHT = 400

        self.freezers_panel = VertContainer(self.canvas, 
                                            10, 
                                            PANELS_Y + PANELS_OFFSET_Y, 
                                            width=self.game.GAME_W // 4, 
                                            height=PANEL_HEIGHT, 
                                            bg_color=DARK_10, 
                                            corner_radius=0, 
                                            pad=(10, 10))

        label1 = Label(self.canvas, 
                       10, 
                       PANELS_Y * .5 + PANELS_OFFSET_Y, 
                       width=self.freezers_panel.width,
                       text="Pannello freezers", 
                       fg_color=TEXT, 
                       corner_radius=0)

        btn1 = TextButton(self.canvas, 
                          x=label1.rect.right, 
                          y=PANELS_Y * .5 + PANELS_OFFSET_Y, 
                          width=label1.height, 
                          height=label1.height,
                          text="+", 
                          fg_color=TEXT, 
                          bg_color="transparent", 
                          hover_color=(20, 20, 20),
                          corner_radius=label1.height // 2,
                          command=lambda: AddFreezerDialogState(self.game, self, self.con, self.cur).enter_state())

        img = load(self.game.assets_dir + "\\sprites\\ui\\refresh.png")
        img = smoothscale(img, (btn1.width, btn1.width))
        btn_refresh = ImageButton(self.canvas, 
                                  x=btn1.rect.right, 
                                  y=PANELS_Y * .5 +
                                  PANELS_OFFSET_Y, 
                                  width=btn1.width, 
                                  height=btn1.width, 
                                  hover_animation=[img],
                                  animation_fps=10,
                                  hover_color=(20, 20, 20),
                                  corner_radius=btn1.height // 2,
                                  command=self.refresh_freezers)

        self.box_panel = VertContainer(
            self.canvas, 
            110 + self.game.GAME_W // 4, 
            PANELS_Y + PANELS_OFFSET_Y, 
            width=self.game.GAME_W // 4, 
            height=PANEL_HEIGHT, 
            bg_color=DARK_10,
            pad=(10, 10), 
            corner_radius=0)

        Label(self.canvas, 
              self.box_panel.x, 
              PANELS_Y * .5 + PANELS_OFFSET_Y,
              width=self.box_panel.width, 
              text="Pannello scatole", 
              fg_color=TEXT, 
              corner_radius=0)

        self.cell_panel = VertContainer(self.canvas, 
                                        210 + 2 * self.game.GAME_W // 4, 
                                        PANELS_Y + PANELS_OFFSET_Y, 
                                        width=self.game.GAME_W // 4, 
                                        height=400, 
                                        bg_color=DARK_10,
                                        pad=(10, 10), 
                                        corner_radius=0)

        Label(self.canvas, 
              self.cell_panel.x, 
              PANELS_Y * .5 + PANELS_OFFSET_Y,
              width=self.cell_panel.width, 
              text="Pannello celle", 
              fg_color=TEXT, 
              corner_radius=0)
        
        # -- Search Bar
        SEARCH_BAR_WIDTH = 600
        self.search_bar = Entry(self.canvas, 
                                self.game.GAME_W // 2 - SEARCH_BAR_WIDTH // 2, 
                                50,
                                width=SEARCH_BAR_WIDTH, 
                                height=30, 
                                bg_color=DARK_10,
                                fg_color=TEXT,
                                placeholder="Ricerca una cellula...",
                                corner_radius=0)
        self.search_btn = TextButton(self.canvas,
                                     self.search_bar.rect.right + 10,
                                     self.search_bar.y,
                                     width=100,
                                     height=30,
                                     fg_color=TEXT,
                                     bg_color=DARK_10,
                                     text="Cerca",
                                     corner_radius=0,
                                     hover_color=DARK,
                                     command=lambda: self.search_cell(self.search_bar.text))

        self.info_msg = Label(self.canvas, 
                              10, 
                              self.game.GAME_H - 50, 
                              width=1000, 
                              text="",
                              font=self.game.font_small,
                              fg_color=WHITE, 
                              bg_color="transparent")
        
        self.refresh_freezers()

    def update(self, dt):
        super().update(dt)
        if self.ci is not None:
            self.ci.update(dt)

    def render(self, surf):
        super().render(surf)
        if self.ci is not None:
            self.ci.render(surf)

    # Database methods
    def init(self):
        self.con = sql.connect("celle.db")
        self.cur = self.con.cursor()

        # Create 'freezers' table
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS freezers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT
                        )"""
        )
        self.con.commit()  # Save changes

        # Create 'scatole' table
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS scatole (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                in_freezer INTEGER NOT NULL,
                                nome TEXT,
                                FOREIGN KEY (in_freezer) REFERENCES freezers(id)
                        )"""
        )
        self.con.commit()  # Save changes

        # Create 'celle' table
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS celle (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                in_scatola INTEGER NOT NULL,
                                in_freezer INTEGER NOT NULL,
                                nome TEXT NOT NULL,
                                tipo TEXT NOT NULL,
                                data TEXT NOT NULL,
                                descrizione TEXT NOT NULL,
                                FOREIGN KEY (in_scatola) REFERENCES scatole(id),
                                FOREIGN KEY (in_freezer) REFERENCES freezers(id)
                        )"""
        )
        self.con.commit()  # Save changes

    def add_freezer_btn(self, frz: Freezer) -> None:
        btn = TextButton(self.canvas, 
                         text=frz.nome, 
                         corner_radius=0,
                         bg_color="transparent",
                         fg_color=TEXT,
                         hover_color=DARK,
                         command=lambda: self.open_freezer_by_id(frz.id))
        frz.btn = btn
        # print(f"Adding freezer {frz.nome} with button {btn}")
        self.freezers[frz.id] = frz
        self.freezers_panel.add_child(btn)

    def search_cell(self, query_string: str) -> None:
        self.cur.execute("""SELECT * FROM celle 
                                   WHERE nome LIKE ? OR 
                                   tipo LIKE ? OR
                                   data LIKE ? OR
                                   descrizione LIKE ?""",
                         (f"%{query_string}%",
                         f"%{query_string}%",
                         f"%{query_string}%",
                         f"%{query_string}%"))
        self.create_result_panel(self.cur.fetchall())
    
    def create_result_panel(self, results: list) -> None:
        self.result_panel = VertContainer(self.canvas,
                                          self.search_bar.x,
                                          self.search_bar.rect.bottom + 10,
                                          width=self.search_bar.width,
                                          bg_color=DARK_20,
                                          corner_radius=0,
                                          pad=(10, 10)
                                          )
        for cell in results:
            txt = f"{cell[3]}, in box di id {cell[1]}, in freezer di id {cell[2]}"
            self.result_panel.add_child(TextButton(self.canvas,
                                                   text=txt,
                                                   fg_color=TEXT,
                                                   bg_color="transparent",
                                                   corner_radius=0,
                                                   hover_color=LIGHT,
                                                   font=self.game.font_small,
                                                   command=partial(self.open_cell_by_id, cell[0])))
        self.result_panel.add_child(TextButton(self.canvas,
                                               text="Chiudi risultati",
                                               bg_color="transparent",
                                               fg_color=ACCENT,
                                               hover_color=BLACK,
                                               corner_radius=0,
                                               font=self.game.font_small,
                                               command=self.destroy_result_panel))
        
    def destroy_result_panel(self):
        if self.result_panel is not None:
            self.result_panel.parent.children.remove(self.result_panel)
            self.result_panel = None

    def open_freezer_by_id(self, _id: int) -> None:
        self.currently_opened_freezer = _id
        frz_ind = self.freezers_panel.children.index(self.freezers[_id].btn)
        self.freezers_panel.children[frz_ind].bg_color = self.freezers_panel.children[frz_ind].original_bg_color = DARK
        for frz in self.freezers_panel.children:
            if frz != self.freezers_panel.children[frz_ind]:
                frz.bg_color = frz.original_bg_color = DARK_10
        self.cur.execute("SELECT * FROM scatole WHERE in_freezer = ?", (_id,))
        boxes = self.cur.fetchall()
        self.box_panel.clear()
        self.box_panel.add_child(TextButton(self.canvas, 
                                            text="Aggiungi scatola", 
                                            corner_radius=0,
                                            bg_color="transparent",
                                            fg_color=TEXT,
                                            hover_color=DARK,
                                            command=lambda: AddBoxDialogState(self.game, self, self.con, self.cur).enter_state()))
        if len(boxes) > 0:
            self._create_box_grid(boxes)
        
        self.cell_panel.clear()
        

    def _create_box_grid(self, boxes):
        cols = 3
        rows = len(boxes) // cols + 1
        BOX_DIM = 100
        self.box_grid = UIGrid(self.canvas,
                               rows=rows,
                               cols=cols,
                               height=BOX_DIM * rows,
                               pad=(10, 10),
                               bg_color=LIGHT,
                               corner_radius=0,
                               border_width=2)
        self.box_panel.add_child(self.box_grid)
        self.box_grid.recalculate_cell_dimensions()
        # This sets (correctly) the width and height of the grid
        self.box_panel.add_child(self.box_grid)
        rows = 3
        
        
        index = row = col = 0
        while index < len(boxes):
            box = boxes[index]
            tb = TextButton(self.canvas,
                       text=box[2],
                       corner_radius=0,
                       font=self.game.font_small,
                       bg_color="transparent",
                       fg_color=TEXT,
                       hover_color=DARK,
                       command = partial(self.open_box_by_id, box[0], row, col))
                    # this should work as well:    command=lambda i=box[0], j=row, k=col: self.open_box_by_id(box[0], row, col))
                    #    command=lambda: self.open_box_v2(tb))
            tb.box = box
            self.box_grid.add_child(tb, row=row, col=col)
            index += 1
            col += 1
            if col >= cols:
                col = 0
                row += 1

    def open_box_by_id(self, _id: int, row: int, col: int):
        """Open a box by its id"""
        # Select the box
        self.currently_opened_box = _id
        self.box_grid.cells[(row, col)].bg_color = self.box_grid.cells[(row, col)].original_bg_color = DARK
       
        # Deselect the other boxes
        for b in self.box_grid.children:
            if b != self.box_grid.cells[(row, col)]:
                b.bg_color = b.original_bg_color = DARK_10
        
        # Get the cells in the box
        self.cur.execute("SELECT * FROM celle WHERE in_scatola = ?", (_id,))
        cells = self.cur.fetchall()
        self.cell_panel.clear()
        self.cell_panel.add_child(TextButton(self.canvas,
                                             text="Aggiungi cella",
                                             fg_color=TEXT,
                                             bg_color="transparent",
                                             corner_radius=0,
                                             hover_color=DARK,
                                             command=self.add_new_cell))
        for cell in cells:
            self.cell_panel.add_child(Label(self.canvas, 
                                            text=cell[3], 
                                            fg_color=TEXT, 
                                            bg_color="transparent",
                                            corner_radius=0))
            
    def open_cell_by_id(self, _id: int) -> None:
        self.cur.execute("SELECT * FROM celle WHERE id = ?", (_id,))
        cella = self.cur.fetchone()
        self.open_freezer_by_id(cella[2])
        print(cella, self.box_grid.cells)
        selected_box_coords = [key for key in self.box_grid.cells.keys() if self.box_grid.cells[key].box[0] == cella[1]][0]

        self.destroy_result_panel()
        self.open_box_by_id(cella[1], selected_box_coords[0], selected_box_coords[1])
        for cell in self.cell_panel.children:
            if cell.text == cella[3]:
                cell.bg_color = LIGHT
                break
    
    def add_new_cell(self):
        self.canvas.toggle_visibility()
        rect = pygame.Rect(0, 0, 0, 0)
        rect.move_ip(self.game.SCREEN_CENTER[0] - 200, self.game.SCREEN_CENTER[1] - 200)
        rect.w = 400
        rect.h = 400
        self.ci = CellInputInterface(self.game, 
                                     rect=rect,
                                     on_close=self.on_cell_input_close)
        
    def on_cell_input_close(self):
        if self.ci.action == "cancel":
            self.canvas.toggle_visibility()
            return
        new_cell = Cella(
            in_scatola=self.currently_opened_box,
            in_freezer=self.currently_opened_freezer,
            nome=self.ci.nome_entry.text,
            tipo=self.ci.tipo_entry.text,
            data=self.ci.data_entry.text,
            descrizione=self.ci.descrizione_entry.text
        )
        self.cur.execute("INSERT INTO celle (in_scatola, in_freezer, nome, tipo, data, descrizione) \
                         VALUES (?, ?, ?, ?, ?, ?)",
                         (new_cell.in_scatola,
                          new_cell.in_freezer,
                          new_cell.nome,
                          new_cell.tipo,
                          new_cell.data,
                          new_cell.descrizione))
        self.con.commit()
        self.canvas.toggle_visibility()
        self.refresh_scatole()
        

    def refresh_freezers(self):
        self.cur.execute("SELECT * FROM freezers")
        freezers = self.cur.fetchall()
        self.freezers_panel.children.clear()
        for freezer in freezers:
            self.add_freezer_btn(Freezer(freezer[1], freezer[0]))

    def refresh_scatole(self):
        if self.currently_opened_freezer is None:
            self.open_freezer_by_id(1)
        else:
            self.open_freezer_by_id(self.currently_opened_freezer)


