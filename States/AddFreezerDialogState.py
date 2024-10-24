from sqlite3 import Connection, Cursor
from States.State import State
from UI.Button import TextButton
from UI.Containers import HorizContainer
from UI.Entry import Entry
from UI.Label import Label
from Utils.Colors import ACCENT, DARK, DARK_10, LIGHT, LIGHT_GREEN, TEXT
from ui_custom import CellInputInterface

import pygame as p


class AddFreezerDialogState(State):
    def __init__(self, game, prev_state, connection: Connection, cursor: Cursor):
        super().__init__(game)
        self.cursor = cursor
        self.connection = connection
        self.prev_state = prev_state

        name_label = Label(self.canvas, 10, 10, width=self.game.GAME_W - 10,
                           text="Nome freezer", fg_color=(255, 255, 255), corner_radius=0)
        self.name_entry = Entry(self.canvas, 
                                self.game.GAME_W * .25, 50, 
                                width=self.game.GAME_W * .5, 
                                height=30, 
                                bg_color=DARK_10,
                                fg_color=TEXT, 
                                corner_radius=0)

        btn_container = HorizContainer(self.canvas,
                                       center=(self.name_entry.rect.centerx, self.name_entry.rect.bottom + 40),
                                       width=400,
                                       height=50,
                                       bg_color="transparent",
                                       pad=(10, 10)
                                       )
        
        ok_button = TextButton(self.canvas,
                               width=200, 
                               height=30, 
                               text="Inserisci",
                               bg_color=DARK_10,
                               fg_color=LIGHT_GREEN,
                               hover_color=DARK, 
                               corner_radius=0,
                               command=self.exit_and_insert)
        
        discard_button = TextButton(self.canvas,
                                    width=200,
                                    height=30,
                                    text="Annulla",
                                    bg_color=DARK_10,
                                    fg_color=ACCENT,
                                    hover_color=LIGHT,
                                    corner_radius=0,
                                    command=self.exit_and_discard
                                    )
        
        btn_container.add_child(ok_button)
        btn_container.add_child(discard_button)

    def exit_and_discard(self):
        self.exit_state()

    def exit_and_insert(self):
        self.cursor.execute(
            "INSERT INTO freezers (nome) VALUES (?)", (self.name_entry.text,))
        self.connection.commit()
        self.prev_state.refresh_freezers()
        self.exit_state()

