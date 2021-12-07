import logging
from game_sdk.gamecontrol import Game
from game_sdk.game import LogLevel
from game_sdk.game_io import GameState


class LedTestGame(Game):
    async def on_score(self):
        scores = self.players.score

        for key, value in scores.items():
            if (value >= 10):
                logging.info("Seat %s wins!!!", key)

                await self.set_game_state(GameState.END)


if __name__ == '__main__':
    game = LedTestGame()
    game.run(log_level=LogLevel.DEBUG)
