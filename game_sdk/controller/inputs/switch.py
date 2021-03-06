import logging
from game_sdk.controller.key_map.gamepad import KeyCode
from .input import Input


class Switch(Input):
    """
        Class for button inputs
    """

    key_bind: KeyCode

    def __init__(self, seat: int, name: str):
        """
            Initializes the switch

            Arguments:
                seat: controller seat
                name: controller name
        """
        super().__init__(seat, name)

    async def on(self, seat: int):
        """
            Called when switch is pressed

            Arguments:
                seat: controller seat
        """

        logging.info("Set switch %s to on", self.name)

    async def off(self, seat: int):
        """
            Called when switch is released

            Arguments:
                seat: controller seat
        """

        logging.info("Set switch %s to off", self.name)
