import asyncio
import logging

from asyncio_mqtt.error import MqttError

from evdev import InputDevice

from game_sdk.game import GameTemplate
from game_sdk.game_io import GameIO, GameState
from game_sdk.controller.inputs import Joystick, Switch
from game_sdk.controller.key_map.gamepad import KeyCode, XBoxWireless


class ControllerNotFoundError(FileNotFoundError):
    pass


class Game(GameTemplate):
    """
        Class to control the whole game. Inherit from this class and call `run()` to start your game
    """

    controls: dict
    ready_control: KeyCode
    _input_dev: InputDevice

    async def _on_pregame(self):
        """
            (Private) Executed, before a new game starts
        """

        for _, control in self.controls.items():
            await control.init(self.config['seat'])

        await self.on_pregame()

    async def _on_end(self):
        """
            (Private) Executed, when the game ends
        """

        for _, control in self.controls.items():
            await control.reset(self.config['seat'])

        await self.on_end()

    async def _on_exit(self, err: Exception = None):
        """
            (Private) Executed, when the game loop is exited

            Arguments:
                err: Value of the exception when the game exited with none zero code
        """

        for _, control in self.controls.items():
            await control.close(self.config['seat'])

        await self.on_exit(err)

    async def _ctl_sub(self):
        """
            Subscribe to gamepad inputs
        """

        try:
            async for ev in self._input_dev.async_read_loop():
                logging.debug("Got controller input - CODE: %d, \tVALUE %d", ev.code, ev.value)
                mapped_code = XBoxWireless.map_key(ev.code)

                if self._game_state is GameState.RUN:
                    if mapped_code in self.controls:
                        control = self.controls[mapped_code]

                        if issubclass(type(control), Switch):
                            if ev.value > 0:
                                asyncio.create_task(control.on(self.config['seat']))
                            else:
                                asyncio.create_task(control.off(self.config['seat']))
                        elif issubclass(type(control), Joystick):
                            asyncio.create_task(control.set_direction(self.config['seat'], ev.value))
                elif self._game_state is GameState.IDLE:
                    if mapped_code is self.ready_control and ev.value > 0:
                        asyncio.create_task(self._game_io.ready(self.config['seat']))
        except OSError:
            raise ControllerNotFoundError()

    async def _game_io_sub(self):
        """
            Subscribe to changes of the game state
        """
        async for game_state in self._game_io.subscribe_to_status():
            logging.debug("Got Gamestate %s", game_state)
            self._game_state = game_state

            if game_state == GameState.START:
                await self._on_pregame()
                asyncio.create_task(self._game_io.ready(self.config['seat']))
            elif game_state == GameState.RUN:
                await self.on_start()
            elif game_state == GameState.END:
                await self._on_end()
                asyncio.create_task(self._game_io.ready(self.config['seat']))

    async def _run(self):
        """
            Asynchronous `run` function
        """
        try:
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
