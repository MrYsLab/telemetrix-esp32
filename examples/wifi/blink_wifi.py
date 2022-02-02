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


"""

import sys
import time

from telemetrix_esp32 import telemetrix_esp32

"""
Setup a pin for digital output 
and toggle the pin 5 times.
"""

# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.232'

DIGITAL_PIN = 2  # the board LED

# Create a Telemetrix instance.
board = telemetrix_esp32.TelemetrixEsp32(transport_address=IP_ADDRESS)

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_digital_output(DIGITAL_PIN)

# Blink the LED and provide feedback as
# to the LED state on the console.
for blink in range(5):
    # When hitting control-c to end the program
    # in this loop, we are likely to get a KeyboardInterrupt
    # exception. Catch the exception and exit gracefully.
    try:
        print('On')
        board.digital_write(DIGITAL_PIN, 0)
        time.sleep(1)
        print('Off')
        board.digital_write(DIGITAL_PIN, 1)
        time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)
