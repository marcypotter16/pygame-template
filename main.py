from Game import Game
from States.LobbyState import LobbyState

g: Game = Game()
g.load_state(LobbyState(g))
g.game_loop()