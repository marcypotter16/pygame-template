from States.State import State
from UI.Label import Label
from math import sin
from time import time

class BlankState(State):
	def __init__(self, game, msg=None, layer="foreground"):
		super().__init__(game, msg, layer)

		# Create a label, it parents itself to self.canvas (inherited from State)
		self.label = Label(self.canvas, center=self.game.SCREEN_CENTER, text="Hi!", width=100, height=50, fg_color=(255, 255, 255))
		
		# Create a circle
		self.circle = Circle(self.game)

	def render(self, surface):
		super().render(surface)

		# Render the circle, the label is automatically rendered by the canvas
		self.circle.render(surface)

	def update(self, delta_time):
		super().update(delta_time)

		# Update the circle, the label is automatically updated by the canvas
		self.circle.update(delta_time)
		
		# Move the label with sine wave
		self.label.rect.y = self.game.SCREEN_CENTER[1] + 5 * sin(time() * 2)

	
from pygame import Vector2
from pygame.draw import circle

class Circle:
	def __init__(self, game, radius = 10):
		self.game = game
		self.position = Vector2(100, 100)
		self.radius = radius

	def render(self, surface):
		circle(surface, color=(255, 255, 255), center=self.position, radius=self.radius)

	def update(self, delta_time):
		self.position.x += 1