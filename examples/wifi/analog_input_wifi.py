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

import sys
import time

from telemetrix_esp32 import telemetrix_esp32

"""
This file demonstrates analog input using both callbacks and
polling. Time stamps are provided in both "cooked" and raw form
"""

# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.232'

# Set up a pin for analog input and monitor its changes
ANALOG_PIN = 36  # gpio pin number


def the_callback(data):
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


def analog_in(my_board, pin):
    """
    This function establishes a pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.


    Also, the differential parameter is being used.
    The callback will only be called when there is
    difference of 150 or more between the current and
    last value reported.

    :param my_board: a telemetrix instance

    :param pin: GPIO pin number
    """
    my_board.set_pin_mode_analog_input(pin, 150, the_callback)
    try:
        while True:
            try:
                time.sleep(.01)
            except KeyboardInterrupt:
                my_board.shutdown()
                sys.exit(0)
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)


the_board = telemetrix_esp32.TelemetrixEsp32(transport_address=IP_ADDRESS)
analog_in(the_board, ANALOG_PIN)
