from sqlite3 import Connection, Cursor
from States.State import State
from UI.Button import TextButton
from UI.Entry import Entry
from UI.Label import Label

class AddCellDialogState(State):
    def __init__(self, game, connection: Connection, cursor: Cursor):
        super().__init__(game)
        self.cursor = cursor
        self.connection = connection

        name_label = Label(self.canvas, 10, 10, width=100, text="Nome", fg_color=(255, 255, 255), corner_radius=0)
        self.name_entry = Entry(self.canvas, 10, 30, width=200, height=30, bg_color=(40, 40, 40), corner_radius=0)
        
        ok_button = TextButton(self.canvas, 10, 70, width=50, height=30, text="OK", corner_radius=10,
                               command=self.exit_state)

    def render(self, surf):
        super().render(surf)

    def update(self, dt):
        super().update(dt)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        self.cursor.execute("INSERT INTO freezers (nome) VALUES (?)", (self.name_entry.text,))
        self.connection.commit()
        super().exit_state()