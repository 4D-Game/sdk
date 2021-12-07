import asyncio
import enum
import logging
from typing import Any, Coroutine, MutableMapping
import toml

from asyncio_mqtt.error import MqttError
from game_sdk.game import GameTemplate

from game_sdk.game_io import GameIO, GameState
from game_sdk.players import Players


class Game(GameTemplate):
    """
        Class to control the whole game. Inherit from this class and call `run()` to start your gamecontrol
    """

    _players: Players

    @property
    def players(self):
        """
            Instance of `Player` used to acces player information
        """

        if self._is_running:
            return self._players
        raise Exception('Execute Game.run() befor accessing player')

    async def set_game_state(self, state: GameState):
        """
            Set `game_state` and execute the coresponding function

            Arguments:
                state: State to wich to switch
        """

        self._game_state = state

        if self._game_state == GameState.START:
            asyncio.create_task(self.on_pregame())
        if self._game_state == GameState.RUN:
            asyncio.create_task(self.on_start())
        if self._game_state == GameState.END:
            asyncio.create_task(self.on_end())

        asyncio.create_task(self._game_io.set_game_state(self._game_state))

    async def on_score(self):
        """
            Executed, when a player scores one or more points
        """

        logging.info("ON SCORE")

    async def _game_io_sub(self):
        """
            Subscribe to changes of the game state

            Arguments:
                mqtt_conf: GameIO configuration
        """

        topic = [('status/ready', 0), ('score', 0)]

        async for topic, data in self._game_io.subscribe(topic):
            logging.debug("Got Message from: %s with %s", topic, data)

            if (topic == "status/ready"):
                self._players.set_ready(data['seat'], data['ready'])
                await self._ready()
            elif (topic == "score") and self._game_state is GameState.RUN:
                self._players.set_score(data['seat'], data['score'])
                asyncio.create_task(self.on_score())

    async def _ready(self):
        """
            Check ready state and change `game_state`
        """

        all_ready = True
        for p_ready in self.players.ready.values():
            all_ready = all_ready and p_ready

        if all_ready:
            logging.debug("All ready")

        if all_ready:
            if self._game_state == GameState.IDLE:
                await self.set_game_state(GameState.START)
            elif self._game_state == GameState.START:
                await self.set_game_state(GameState.RUN)
            elif self._game_state == GameState.END:
                await self.set_game_state(GameState.IDLE)

            self._players.reset_ready()

    async def _run(self):
        """
            Asynchronous `run` function
        """
        try:
            self._players = Players(self.config['seats'])

            self._game_io = GameIO(self.config['MQTT'])
            await self._game_io.connect()

            main_loop = asyncio.gather(
                self._game_io_sub()
            )

            await self.on_init()
            self._is_running = True

            # try:
            await main_loop
            await self.on_exit()
            # except Exception as err:
            #    await self.on_exit(err)
        except MqttError:
            logging.error("Couldn't connect to MQTT Client")
            logging.error("MQTT Config: %s", self.config['MQTT'])
