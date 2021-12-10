import logging
from game_sdk.controller.key_map.gamepad import JoystickCode
from game_sdk.controller.inputs import Input


class Joystick(Input):
    """
        Class for all joystick inputs
    """

    THRESHHOLD: float = 0.1
    _last_pos = 0

    def __init__(self, seat: int, name: str):
        """
            Initializes the joystick

            Arguments:
                seat: controller seat
                name: controller name
        """
        super().__init__(seat, name)

    def _map_position(self, pos: int) -> float:
        return (pos / 32768) - 1

    async def set_direction(self, seat: int, pos: int):
        mapped_pos = self._map_position(pos)

        self._last_pos = mapped_pos

        if ((- self.THRESHHOLD) < mapped_pos < (self.THRESHHOLD)):
            logging.debug("Threshold reached")
            self._last_pos = 0

        await self.get_direction(seat, self._last_pos)

    async def get_direction(self, seat: int, pos: float):
        """
            Called with directions from the joystick

            Arguments:
                pos: coordinate of movement (from -1 to 1)
        """

        logging.info("Set direction of %s to %s", self.name, pos)
