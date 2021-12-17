#!/usr/bin/env python3

from game_sdk.controller import Game
from game_sdk.game import LogLevel
from game_sdk.controller.inputs import Joystick, Switch
from game_sdk.controller.key_map import JoystickCode, KeyCode


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
