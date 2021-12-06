import logging
from game_sdk.key_map.gamepad import JoystickCode
from game_sdk.inputs import Input


class Joystick(Input):
    """
        Class for all joystick inputs
    """

    joystick_pos: JoystickCode
    threshhold: float = 0.1
    last_pos = 0

    def __init__(self, seat: int, name: str):
        """
            Initializes the joystick

            Arguments:
                seat: controller seat
                name: controller name
                joystick_pos = joystick position, x&y coordinates
        """
        super().__init__(seat, name)

    def _mapPosition(self, pos: int) -> float:
        return (pos / 32768) - 1

    async def set_direction(self, seat: int, pos: int):
        mapped_pos = self._mapPosition(pos)

        self.last_pos = mapped_pos

        if ((- self.threshhold) < mapped_pos < (self.threshhold)):
            logging.debug("Threshold reached")
            self.last_pos = 0

        await self.get_direction(seat, self.last_pos)

    async def get_direction(self, seat: int, pos: float):
        """
            Called with directions from the joystick

            Arguments:
                x: x-coordinate of movement (from -1 to 1)
                y: y-coordinate of movement (from -1 to 1)
        """

        logging.info("Set direction of %s to %s", self.name, pos)
