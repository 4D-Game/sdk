import logging
from typing import Callable
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from game_sdk.controller.key_map import KeyCode
from game_sdk.controller import Game
from game_sdk.controller.inputs import Switch

LED_PIN = 17


class ReadySwitch(Switch):
    """
        Input class to configure ready button
    """

class LEDSwitch(Switch):
    """
        Input class wich switches LED on and off
    """

    def __init__(self, seat: int, name: str, score_cb: Callable = None):

        # Initialize LED pin
        GPIO.setup(LED_PIN, GPIO.OUT)
        # Store reference to score callback function
        self.score_cb = score_cb
        super().__init__(seat, name)

    async def on(self, seat=0):
        """
            Switch LED on
        """

        GPIO.output(LED_PIN, GPIO.HIGH)
        await self.score_cb()

    async def off(self, seat=0):
        """
            Switch LED off
        """

        GPIO.output(LED_PIN, GPIO.LOW)

    async def reset(self, seat=0):
        """
            Switch LED off when the game ends
        """

        await self.off(seat)

    async def close(self, seat):
        """
            Turn LED off and reset GPIO configuration
        """

        # Set LED pin into safe state by setting it to input mode
        await self.off(seat)
        GPIO.setup(LED_PIN, GPIO.IN)
        GPIO.cleanup()


class LedTestGame(Game):
    """
        Gameclass for the testgame
    """

    score = 0

    async def update_score(self):
        """
            Increase score and publish new score
        """

        self.score += 1
        await self.game_io.score(score=self.score, seat=self.config["seat"])

    async def on_init(self):
        """
            Register inputs and ready control
        """

        self.ready_control = {KeyCode.BUT_1: ReadySwitch(self.config['seat'], 'ReadySwitch')}
        # Register LED input with update score callback function
        self.controls = {KeyCode.BUT_0: LEDSwitch(self.config["seat"], 'LEDSwitch_1', self.update_score)}

    async def on_pregame(self):
        """
            Reset score
        """

        # Set score to 0 before game starts
        self.score = 0


if __name__ == "__main__":
    # Start running the game
    LedTestGame().run("/home/pi/Controller/config.toml")
