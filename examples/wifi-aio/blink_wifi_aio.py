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
Setup a pin for digital output and output a signal
and toggle the pin. Do this 4 times.
"""
# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.215'

# some globals
DIGITAL_PIN = 23  # gpio pin number


async def blink(my_board, pin):
    """
    This function will to toggle a digital pin.

    :param my_board: a telemetrix instance
    :param pin: GPIO pin to be controlled
    """

    # set the pin mode
    await my_board.set_pin_mode_digital_output(pin)

    # toggle the pin 4 times and exit
    for x in range(4):
        print('ON')
        await my_board.digital_write(pin, 0)
        await asyncio.sleep(1)
        print('OFF')
        await my_board.digital_write(pin, 1)
        await asyncio.sleep(1)


# get the event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# instantiate telemetrix
board = telemetrix_aio_esp32.TelemetrixAioEsp32(transport_address=IP_ADDRESS)

try:
    # start the main function
    loop.run_until_complete(blink(board, DIGITAL_PIN))
    loop.run_until_complete(board.shutdown())

except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
