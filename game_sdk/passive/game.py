import asyncio
import logging
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

        topic = [("score", 0), ("status/game", 0)]

        async for topic, data in self._game_io.subscribe(topic):
            logging.debug("Got Message from: %s with %s", topic, data)

            if (topic == "score") and self._game_state is GameState.RUN:
                self._players.set_score(data['seat'], data['score'])
                asyncio.create_task(self.on_score())
            elif (topic == "status/game"):
                mode = data['mode'] if 'mode' in data else 'idle'

                game_state = GameState.IDLE
                if mode == 'start':
                    game_state = GameState.START
                elif mode == 'run':
                    game_state = GameState.RUN
                elif mode == 'end':
                    game_state = GameState.END
                 
                logging.debug("Got Gamestate %s", game_state)
                self._game_state = game_state

                if game_state == GameState.START:
                    await self.on_pregame()
                elif game_state == GameState.RUN:
                    await self.on_start()
                elif game_state == GameState.END:
                    await self.on_end()

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
            # except Exception as err:
            #    await self.on_exit(err)
        except MqttError:
            logging.error("Couldn't connect to MQTT Client")
            logging.error("MQTT Config: %s", self.config['MQTT'])
