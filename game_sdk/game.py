import enum
import logging
import asyncio
from typing import Any, MutableMapping

import toml

from game_sdk import GameIO
from game_sdk.game_io import GameState


class LogLevel(enum.Enum):
    """
        Different logging levels defiend by the logging module
    """

    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class GameTemplate:
    """
      Template for the different Game classes

      Attributes:
        config: contains the configuration from the config file
    """

    config: MutableMapping[str, Any]
    _is_running = False
    _game_io: GameIO
    _game_state = GameState.IDLE

    @property
    def game_io(self):
        """
            Instance of `GameIO` used to control the whole game loop
        """

        if self._is_running:
            return self._game_io
        raise Exception('Execute Game.run() before accessing game_io')

    @property
    def game_state(self):
        """
          State of the game
        """

        return self.game_state

    async def on_init(self):
        """
            Executed, when the game is startet with `Game.run()`
        """

        logging.info("ON INIT")

    async def on_pregame(self):
        """
            Executed, before a new game starts
        """

        logging.info("ON PREGAME")

    async def on_start(self):
        """
            Executed, when a new game starts
        """
        logging.info("ON START")

    async def _on_end(self):
        """
            (Private) Executed, when the game ends
        """

        await self.on_end()

    async def on_end(self):
        """
            Executed, when the game ends
        """

        logging.info("ON END")

    async def _on_exit(self, err: Exception = None):
        """
            (Private) Executed, when the game loop is exited

            Arguments:
                err: Value of the exception when the game exited with none zero code
        """

    async def on_exit(self, err: Exception = None):
        """
            Executed, when the game loop is exited

            Arguments:
                err: Value of the exception when the game exited with none zero code
        """

        logging.info("ON EXIT")

        if err:
            logging.error(err)

    async def _run(self):
        """
            Asynchronous `run` function
        """

    def run(self, conf_path: str = '/home/pi/Gamecontrol/config.toml', log_level: LogLevel = LogLevel.NOTSET):
        """
            Start the game engine

            Arguments:
                conf_path: Path to configuration.toml
                log_level: logging level
        """

        logging.getLogger().setLevel(log_level.value)

        try:
            self.config = toml.load(conf_path)
            logging.info("Config: \n%s", self.config)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._run())
        except FileNotFoundError:
            logging.error("No config found at: %s", conf_path)
        except KeyboardInterrupt:
            logging.info("Keyboard Interrupt")
        finally:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._on_exit())
