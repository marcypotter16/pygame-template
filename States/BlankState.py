from States.State import State
from UI.Label import Label
from math import sin
from time import time

class BlankState(State):
	def __init__(self, game, msg=None, layer="foreground"):
		super().__init__(game, msg, layer)

		self.label = Label(self.canvas, center=self.game.SCREEN_CENTER, text="Hi!", width=100, height=50, fg_color=(255, 255, 255))

	def render(self, surface):
		super().render(surface)

	def update(self, delta_time):
		super().update(delta_time)
		
		# Move the label with sine wave
		self.label.rect.y = self.game.SCREEN_CENTER[1] + 5 * sin(time() * 2)