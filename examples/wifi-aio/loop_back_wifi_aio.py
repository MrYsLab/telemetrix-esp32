"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

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
Loopback some data to assure that data can be sent and received between
the Telemetrix client and Telemetrix server.
"""


async def the_callback(data):
    """
    A callback function to report receive the looped back data

    :param data: [looped back data]
    """
    print(f'Looped back: {chr(data[0])}')


async def loop_back(my_board, loop_back_data):
    """
    This function will request that the supplied characters be
    sent to the board and looped back and printed out to the console.

    :param my_board: a pymata4 instance
    :param loop_back_data: A list of characters to have looped back
    """
    try:
        for data in loop_back_data:
            await my_board.loop_back(data, callback=the_callback)
            print(f'Sending: {data}')
            await asyncio.sleep(.1)
        # await my_board.shutdown()
        # sys.exit(0)
    except KeyboardInterrupt:
        await my_board.shutdown()
        sys.exit(0)

# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = telemetrix_aio_esp32.TelemetrixAioEsp32(
    transport_is_ble=False, transport_address='192.168.2.232')
char_list = ['A', 'B', 'Z']
try:
    # start the main function
    loop.run_until_complete(loop_back(board, char_list))
    loop.run_until_complete(board.shutdown())
    sys.exit(0)

except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)

