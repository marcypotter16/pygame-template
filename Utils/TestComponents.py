from Game import Game

def test_state(state):
    g = Game()
    g.push_state(state)
    g.game_loop()

if __name__ == '__main__':
    pass
