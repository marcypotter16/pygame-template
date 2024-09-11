from pygame import Surface
from States.State import State
from UI.Entry import Entry

class LobbyState(State):
	def __init__(self, game, msg=None, layer="foreground"):
		super().__init__(game, msg, layer)

		# Create UI elements
		# self.msg_label: Label = Label(self, center=(self.game.width // 2, self.game.height // 2 - 100), text="Enter message", font_size=40)
		self.msg_entry: Entry = Entry(self.canvas, center=(self.game.GAME_W // 2, self.game.GAME_H // 2), width=400, height=50, placeholder="Enter message", corner_radius=10, is_password=False)
		self.msg_entry.set_enter_key_callback(lambda: print("Enter key pressed"))
		# Add UI elements to the canvas
		# self.canvas.add_child(self.msg_entry)

	def render(self, surface: Surface):
		return super().render(surface)
	
	def update(self, dt: float):
		return super().update(dt)
	