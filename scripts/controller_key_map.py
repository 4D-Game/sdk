#!/usr/bin/env python3

"""
Created: 12.12.21
by: Lukas Schüttler

Check functionallity and key codes of a gamepad
"""

import asyncio
import logging

from evdev import InputDevice


async def main():
    input_dev = InputDevice("/dev/input/event1")
    logging.info(f"Device connected: {input_dev}")

    try:
        async for ev in input_dev.async_read_loop():
            logging.debug("Got controller input - CODE: %d, \tVALUE %d", ev.code, ev.value)
    except OSError:
        logging.warning("Controller disconnected")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main())
