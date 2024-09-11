# A template for object oriented game making with [pygame](https://www.pygame.org/)

## Quickstart

Create a file in the "States" folder, write a class that extends State, look "BlankState" for an easy example.
You can attach UI elements to the state just by creating them as members of the class.

Every entity in the game has two important methods:
* `update(self, dt: float)`
* `render(self, surface: pygame.Surface)`
  
and a property `game`, which is useful for many reasons.

For example I can create a class Circle
```python
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
```

and put it in a State
```python
from States.State import State

class SomeState(State):
	def __init__(self, game, msg=None, layer="foreground"):
		super().__init__(game, msg, layer)

		self.circle = Circle(self.game)

	def render(self, surface):
		super().render(surface)
		self.circle.render(surface)

	def update(self, delta_time):
		super().update(delta_time)
		self.circle.update(delta_time)

```

Then you can just run `main.py` with the following code:
```python
from Game import Game
from States.SomeState import SomeState

g = Game()
g.load_state(SomeState(g))
g.game_loop()

```