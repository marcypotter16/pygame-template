from Game import Game
from GameManagerOffline import GameManagerOffline
from States.BattleOfflineTest import BattleOfflineTest


def test_state(state):
    g = Game()
    g.push_state(state)
    g.game_loop()


if __name__ == '__main__':
    g = Game(workdir="C:/Users/marcy/PycharmProjects/cards")
    test_state(BattleOfflineTest(g, GameManagerOffline(g)))
