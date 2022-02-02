"""
 Copyright (c) 2022 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 DHT support courtesy of Martyn Wheeler
 Based on the DHTNew library - https://github.com/RobTillaart/DHTNew
"""

import sys
import time

from telemetrix_esp32 import telemetrix_esp32

"""
Setup a pin for output and fade its intensity
"""

# some globals
# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.232'

# make sure to select a PWM pin
DIGITAL_PIN = 2
CHANNEL = 0


def fade(board, pin):
    """
    Perform the PWM fade

    :param board: telemetrix instance
    :param pin: gpio pin
    """

    # Set the DIGITAL_PIN as an output pin
    board.set_pin_mode_analog_output(pin)
    board.analog_write(CHANNEL, 0)
    # When hitting control-c to end the program
    # in this loop, we are likely to get a KeyboardInterrupt
    # exception. Catch the exception and exit gracefully.

    try:
        print('Fading up...')
        for i in range(0, 255, 5):
            board.analog_write(CHANNEL, i)
            time.sleep(.1)
        print('Fading down...')
        for i in range(255, -1, -5):
            board.analog_write(CHANNEL, i)
            time.sleep(.1)
        board.analog_write(CHANNEL, 0)
        board.detach_pin_to_analog_channel(DIGITAL_PIN, CHANNEL)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)


# instantiate telemetrix
the_board = telemetrix_esp32.TelemetrixEsp32(transport_address=IP_ADDRESS)

try:
    # start the main function
    fade(the_board, DIGITAL_PIN)
    the_board.shutdown()
except KeyboardInterrupt:
    the_board.shutdown()
    sys.exit(0)
