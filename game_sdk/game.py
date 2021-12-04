import asyncio
from asyncio.tasks import create_task
import enum
import logging
import atexit
from typing import Any, MutableMapping, Type

from asyncio_mqtt.error import MqttError

from evdev import InputDevice, categorize, ecodes
import toml

from game_sdk.game_io import GameIO, GameState
from game_sdk.inputs.input import Input
from game_sdk.inputs.joystick import Joystick
from game_sdk.inputs.switch import Switch
from game_sdk.key_map.gamepad import KeyCode, XBoxWireless


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


class ControllerNotFoundError(FileNotFoundError):
    pass


class Game:
    """
        Class to control the whole game. Inherit from this class and call `run()` to start your game
    """

    controls: dict
    ready_control: KeyCode
    config: MutableMapping[str, Any]
    game_state = GameState.IDLE
    _input_dev: InputDevice
    _is_running = False
    _game_io: GameIO

    @property
    def game_io(self):
        """
           Instance of `GameIO` used to control the whole game loop
        """

        if self._is_running:
            return self._game_io
        raise Exception('Execute Game.run() before accessing game_io')

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

        for _, control in self.controls.items():
            await control.reset(self.config['seat'])

        await self.on_end()

    async def on_end(self):
        """
            Executed, when the game ends
        """

        logging.info("ON END")

    def _atexit(self):
        """
            Synchronous function to call `on_exit()`
        """

        self._on_exit()

    async def _on_exit(self, err: Exception = None):
        """
            (Private) Executed, when the game loop is exited

            Arguments:
                err: Value of the exception when the game exited with none zero code
        """

        for _, control in self.controls.items():
            await control.close(self.config['seat'])

        await self.on_exit(err)

    async def on_exit(self, err: Exception = None):
        """
            Executed, when the game loop is exited

            Arguments:
                err: Value of the exception when the game exited with none zero code
        """

        logging.info("ON EXIT")

        if err:
            logging.error(err)

    async def _ctl_sub(self):
        """
            Subscribe to gamepad inputs
        """

        try:
            async for ev in self._input_dev.async_read_loop():
                logging.debug("Got controller input - CODE: %d, \tVALUE %d", ev.code, ev.value)
                mapped_code = XBoxWireless.mapKey(ev.code)

                if self.game_state is GameState.RUN:
                    if mapped_code in self.controls:
                        control = self.controls[mapped_code]

                        if issubclass(type(control), Switch):
                            if ev.value > 0:
                                asyncio.create_task(control.on(self.config['seat']))
                            else:
                                asyncio.create_task(control.off(self.config['seat']))
                        elif issubclass(type(control), Joystick):
                            asyncio.create_task(control.set_direction(self.config['seat'], ev.value))
                elif self.game_state is GameState.IDLE:
                    if mapped_code is self.ready_control and ev.value > 0:
                        asyncio.create_task(self._game_io.ready(self.config['seat']))
        except OSError:
            raise ControllerNotFoundError()

    async def _game_io_sub(self):
        """
            Subscribe to changes of the game state
        """
        async for game_state in self._game_io.subscribe():
            logging.debug("Got Gamestate %s", game_state)
            self.game_state = game_state

            if game_state == GameState.START:
                await self.on_pregame()
                asyncio.create_task(self._game_io.ready(self.config['seat']))
            elif game_state == GameState.RUN:
                await self.on_start()
            elif game_state == GameState.END:
                await self._on_end()
                asyncio.create_task(self._game_io.ready(self.config['seat']))

    async def _run(self, conf_path: str = '/home/pi/Controller/config.toml'):
        """
            Asynchronous `run` function
        """
        try:
            self.config = toml.load(conf_path)
            logging.debug(self.config)

            # Init GameIO
            self._game_io = GameIO(self.config['MQTT'])
            await self._game_io.connect()

            # Connect Device
            try:
                self._input_dev = InputDevice(self.config['CONTROLLER']['input_device'])
            except FileNotFoundError:
                raise ControllerNotFoundError

            # atexit.register(self._atexit)

            main_loop = asyncio.gather(
                self._ctl_sub(),
                self._game_io_sub()
            )

            self._is_running = True
            await self.on_init()

            #  try:
            await main_loop
            # except Exception as err:
            #     self._on_exit(err)

        except MqttError:
            logging.error("Couldn't connect to MQTT Client")
            logging.error("MQTT Config: %s", self.config['MQTT'])
        except ControllerNotFoundError:
            logging.error("Couldn't connect to Gamepad")
            logging.error("Gamepad Config: %s", self.config['CONTROLLER'])
        except FileNotFoundError:
            logging.error("No config found at: %s", conf_path)

    def run(self, conf_path: str = '/home/pi/Controller/config.toml', log_level: LogLevel = LogLevel.NOTSET):
        """
            Start the game engine

            Arguments:
                conf_path: Path to configuration.toml
                log_level: logging level
        """

        logging.getLogger().setLevel(log_level.value)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._run(conf_path))
        except KeyboardInterrupt:
            logging.info("Keyboard Interrupt")
        finally:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._on_exit())
