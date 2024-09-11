from Game import Game
from States.BlankState import BlankState

g: Game = Game()
g.load_state(BlankState(g))
g.game_loop()