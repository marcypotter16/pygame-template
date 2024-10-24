from sqlite3 import Connection, Cursor
from States.State import State
from UI.Button import TextButton
from UI.Containers import HorizContainer
from UI.Entry import Entry
from UI.Grid import UIGrid
from UI.Label import Label
from Utils.Colors import *
from models import Cella
from ui_custom import CellInputInterface
import pygame as p

CII_WIDTH = 400
CII_HEIGHT = 400

class AddBoxDialogState(State):
    def __init__(self, game, prev_state, connection: Connection, cursor: Cursor):
        super().__init__(game)

        # TODO: Match the palette from the other window

        self.cursor = cursor
        self.connection = connection
        self.prev_state = prev_state
        self.selected_coords: tuple[int, int] = None
        self.altered_cells: dict[tuple[int, int], Cella] = {}

        GRID_ROWS = 10
        GRID_COLS = 15

        name_label = Label(self.canvas, 
                           10, 
                           10, 
                           width=self.game.GAME_W - 10,
                           text="Nome scatola", 
                           fg_color=TEXT, 
                           corner_radius=0)
        self.name_entry = Entry(self.canvas, 
                                self.game.GAME_W * .25, 
                                50, 
                                width=self.game.GAME_W * .5, 
                                height=30, 
                                bg_color=DARK_10, 
                                fg_color=TEXT,
                                corner_radius=0)
        
        self.ci: CellInputInterface = None
        

        buttons_group = HorizContainer(self.canvas,
                                       center=(self.game.GAME_W // 2, self.game.GAME_H - 50),
                                        width=440,
                                        height=30,
                                        bg_color="transparent",
                                        corner_radius=0,
                                        pad=(10, 0))
        ok_button = TextButton(self.canvas, 
                               width=200, 
                               height=30, 
                               text="Inserisci",
                               bg_color=DARK_10,
                               fg_color=LIGHT_GREEN,
                               hover_color=DARK,
                               corner_radius=0,
                               command=self.on_ok_button_click)
        buttons_group.add_child(ok_button)
        annulla_button = TextButton(self.canvas,
                                    width=200,
                                    height=30,
                                    text="Annulla",
                                    bg_color=DARK_10,
                                    fg_color=ACCENT,
                                    hover_color=DARK,
                                    corner_radius=0,
                                    command=self.exit_state)
        buttons_group.add_child(annulla_button)
                                    
        
        self.grid = UIGrid(self.canvas,
                           center=p.Vector2(self.game.SCREEN_CENTER),
                           width=600,
                           height=400,
                           rows=GRID_ROWS,
                           cols=GRID_COLS,
                           bg_color=DARK_10,
                           corner_radius=0,
                           pad=(10, 10))
        for i in range(self.grid.rows * self.grid.cols):
            r, c = i // self.grid.cols, i % self.grid.cols
            self.grid.add_child(
                TextButton(self.canvas, 
                           text=f"{i}",
                           font=self.game.font_small,
                           fg_color=p.Vector3(TEXT) * 0.5,
                           bg_color="transparent",
                           hover_color=DARK,
                           corner_radius=0,
                           command=lambda i=r, j=c: self.on_cell_click(i, j)), 
                    r, 
                    c)

        Label(self.canvas,
              x=self.grid.rect.left,
              y=self.grid.rect.top - 45,
              width=600,
              height=30,
              fg_color=WHITE,
              text="Cellule nella scatola (fai click per aggiungere una cellula)")

    def render(self, surf):
        super().render(surf)
        if self.ci and self.ci.visible:
            self.ci.render(surf)

    def update(self, dt):
        super().update(dt)
        if self.ci and self.ci.visible:
            self.ci.update(dt)

    def enter_state(self):
        super().enter_state()
        print("Entering AddBoxDialogState, state stack: ", self.game.state_stack)

    def exit_state(self):
        self.prev_state.refresh_scatole()
        print("Exiting AddBoxDialogState, state stack: ", self.game.state_stack)
        super().exit_state()

    def on_cell_click(self, row, col):
        rect = p.Rect(
            self.game.SCREEN_CENTER[0] - CII_WIDTH // 2,
            self.game.SCREEN_CENTER[1] - CII_HEIGHT // 2,
            CII_WIDTH,
            CII_HEIGHT
        )
        self.ci = CellInputInterface(self.game, rect=rect, on_close=self.on_cell_input_close)
        self.selected_coords = (row, col)
        self.canvas.toggle_visibility()

    def on_cell_input_close(self):
        if self.ci.action == "cancel":
            self.canvas.toggle_visibility()
            return
        self.altered_cells[self.selected_coords] = Cella(
            in_scatola=None,
            in_freezer=self.prev_state.currently_opened_freezer,
            nome=self.ci.nome_entry.text,
            tipo=self.ci.tipo_entry.text,
            data=self.ci.data_entry.text,
            descrizione=self.ci.descrizione_entry.text
        )
        cell = self.grid.cells[self.selected_coords]
        cell.fg_color = ACCENT
        cell.bg_color = cell.original_bg_color = LIGHT
        print(self.altered_cells)
        self.canvas.toggle_visibility()

    def on_ok_button_click(self):
        print("OK button clicked")
        print(self.name_entry.text, self.prev_state.currently_opened_freezer)
        self.cursor.execute(
            'INSERT INTO scatole (in_freezer, nome) VALUES (?, ?)', (self.prev_state.currently_opened_freezer, self.name_entry.text)
        )
        self.connection.commit()
        box_id = self.cursor.lastrowid
        for coords, cell in self.altered_cells.items():
            self.cursor.execute(
                """
                INSERT INTO celle (in_freezer, in_scatola, nome, tipo, data, descrizione, riga, colonna)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cell.in_freezer,
                 box_id,
                 cell.nome,
                 cell.tipo,
                 cell.data,
                 cell.descrizione,
                 coords[0],
                 coords[1])
            )
        self.connection.commit()
        self.exit_state()