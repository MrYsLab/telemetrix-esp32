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
import time

from telemetrix_aio_esp32 import telemetrix_aio_esp32

"""
This file demonstrates analog inputs
"""

# Set up a pin for analog input and monitor its changes
ANALOG_PIN = 36  # gpio pin number


async def the_callback(data):
    """
    A callback function to report data changes.

    :param data: [pin_mode, pin, current_reported_value,  timestamp]
    """

    # Callback data indices
    CB_PIN = 1
    CB_VALUE = 2
    CB_TIME = 3

    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Analog Call Input Callback: pin={data[CB_PIN]}, '
          f'Value={data[CB_VALUE]} Time={formatted_time} '
          f'(Raw Time={data[CB_TIME]})')


async def analog_in(my_board, pin):
    """
    This function establishes a pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.


    Also, the differential parameter is being used.
    The callback will only be called when there is
    difference of 100 or more between the current and
    last value reported.

    :param my_board: a telemetrix instance

    :param pin: GPIO pin number
    """
    await my_board.set_pin_mode_analog_input(pin, 100, the_callback)

    try:
        while True:
            try:
                await asyncio.sleep(.01)
            except KeyboardInterrupt:
                await my_board.shutdown()
                sys.exit(0)

    except KeyboardInterrupt:
        await my_board.shutdown()
        sys.exit(0)


# get the event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# instantiate telemetrix
board = telemetrix_aio_esp32.TelemetrixAioEsp32(transport_is_wifi=False)

# start the main function
try:
    loop.run_until_complete(analog_in(board, ANALOG_PIN))
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
