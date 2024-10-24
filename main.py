from Game import Game
from States.BezierTestState import BezierTestState

g: Game = Game()
g.load_state(BezierTestState(g))
g.game_loop()