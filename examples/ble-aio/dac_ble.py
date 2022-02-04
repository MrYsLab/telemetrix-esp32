"""
 Copyright (c) 2022 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import asyncio
import sys

from telemetrix_aio_esp32 import telemetrix_aio_esp32

"""
Setup pin 25 for DAC operation and set voltage to 1.65 volts.

Wait for 5 seconds and then disable the DAC.
"""

# some globals
DAC_PIN = 25  # board LED


async def dac(my_board, pin, value):
    """
    This function will set the voltage for a dac pin

    :param my_board: a telemetrix instance
    :param pin: pin to be controlled
    :param value: 0 - 255
    """

    # set the pin mode
    await my_board.set_pin_mode_dac(pin, value)

    await asyncio.sleep(5)

    await my_board.dac_disable(pin)


# get the event loop
loop = asyncio.get_event_loop()

# instantiate telemetrix
board = telemetrix_aio_esp32.TelemetrixAioEsp32(transport_is_wifi=False)

try:
    # start the main function
    loop.run_until_complete(dac(board, DAC_PIN, 128))
    loop.run_until_complete(board.shutdown())

except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
