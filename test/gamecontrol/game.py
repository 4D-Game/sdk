from game_sdk.gamecontrol import Game
from game_sdk.game import LogLevel

if __name__ == '__main__':
    game = Game()
    game.run(log_level=LogLevel.DEBUG)
