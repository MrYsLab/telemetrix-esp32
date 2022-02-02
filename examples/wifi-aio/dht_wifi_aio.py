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
This program monitors a DHT 11 humidity/temperature sensor
"""

# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.232'

DHT_PIN = 13  # GPIO pin


# A callback function to display the distance
# indices into callback data for valid data
# REPORT_TYPE = 0
# READ_RESULT = 1
# PIN = 2
# DHT_TYPE = 3
# HUMIDITY = 4
# TEMPERATURE = 5
# TIME = 6

# indices into callback data for error report
# REPORT_TYPE = 0
# READ_RESULT = 1
# PIN = 2
# HUMIDITY = 3
# TEMPERATURE = 4
# TIME = 5
# noinspection GrazieInspection
async def the_callback(data):
    # noinspection GrazieInspection
    """
        The callback function to display the change in distance
        :param data: [report_type = PrivateConstants.DHT, error = 0, pin number,
                      humidity, temperature timestamp]
                     if this is an error report:
                     [report_type = PrivateConstants.DHT, error != 0, pin number,
                     timestamp]
        """
    if data[1]:
        # error message
        # date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[4]))
        # print(f'DHT Error Report:'
        #   f'Pin: {data[2]} Error: {data[1]}  Time: {date}')
        # just ignore errors
        pass
    else:
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[5]))
        print(f'DHT Valid Data Report:'
              f'Pin: {data[2]}  Humidity: {data[3]} Temperature:'
              f' {data[4]} Time: {date}')


async def dht(my_board, pin):
    # noinspection GrazieInspection
    """
        Set the pin mode for a DHT device. Results will appear via the
        callback.

        :param my_board: a telemetrix instance

        :param pin: GPIO pin

        """

    # set the pin mode for the DHT device
    await my_board.set_pin_mode_dht(pin, the_callback)

    # just sit in a loop waiting for the reports to come in
    while True:
        try:
            await asyncio.sleep(.001)
        except KeyboardInterrupt:
            my_board.shutdown()
            sys.exit(0)


# get the event loop
loop = asyncio.get_event_loop()

# instantiate telemetrix
board = telemetrix_aio_esp32.TelemetrixAioEsp32(transport_address=IP_ADDRESS)
try:
    loop.run_until_complete(dht(board, DHT_PIN))
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
