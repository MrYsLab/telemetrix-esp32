"""
 Copyright (c) 2023 Alan Yorinks All rights reserved.

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

import sys
import time
from telemetrix_esp32 import telemetrix_esp32

"""
Loopback some data to assure that data can be sent and received between
the Telemetrix client and Telemetrix server.
"""


def the_callback(data):
    """
    A callback function to report receive the looped back data

    :param data: [looped back data]
    """
    print(f'Looped back: {chr(data[0])}')


def loop_back(my_board, loop_back_data):
    """
    This function will request that the supplied characters be
    sent to the board and looped back and printed out to the console.

    :param my_board: a telemetrix instance
    :param loop_back_data: A list of characters to have looped back
    """
    try:
        print(f'Sending {char_list}')
        for data in loop_back_data:
            my_board.loop_back(data, callback=the_callback)
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)


# instantiate telemetrix
board = telemetrix_esp32.TelemetrixEsp32(transport_is_wifi=False)

char_list = ['A', 'B', 'Z']

try:
    # start the main function
    loop_back(board, char_list)
    time.sleep(2)
    board.shutdown()
    sys.exit(0)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
