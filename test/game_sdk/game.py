#!/usr/bin/env python3

import logging
from game_sdk import Game
from game_sdk.game import LogLevel
import asyncio
from game_sdk.inputs.joystick import Joystick

from game_sdk.inputs.switch import Switch
from game_sdk.key_map.gamepad import JoystickCode, KeyCode


class TestSwitch(Switch):
    pass


class TestDir(Joystick):
    pass


class GameTest(Game):
    async def on_init(self):
        self.controls = {
            KeyCode.R2: TestSwitch(self.config['seat'], 'TestSwitch'),
            JoystickCode.LEFT_Y: TestDir(self.config['seat'], 'TestJoystick')
        }

        self.ready_control = KeyCode.BUT_1

        return await super().on_init()

    async def on_pregame(self):
        return await super().on_pregame()

    async def on_start(self):
        return await super().on_start()


if __name__ == "__main__":
    test_game = GameTest()
    test_game.run(log_level=LogLevel.DEBUG)
