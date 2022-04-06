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
Run a motor continuously without acceleration

Motor used to test is a NEMA-17 size - 200 steps/rev, 12V 350mA.
And the driver is a TB6600 4A 9-42V Nema 17 Stepper Motor Driver.

The driver was connected as follows:
VCC 12 VDC
GND Power supply ground
ENA- Not connected
ENA+ Not connected
DIR- ESP32 GND
DIR+ GPIO Pin 23 ESP32
PUL- ESP32 GND
PUL+ GPIO Pin 22 ESP32
A-, A+ Coil 1 stepper motor
B-, B+ Coil 2 stepper motor
"""

# GPIO Pins
PULSE_PIN = 22
DIRECTION_PIN = 23


def step_continuous(the_board):
    # create an accelstepper instance for a TB6600 motor driver
    # if you are using a micro stepper controller board:
    # pin1 = pulse pin, pin2 = direction
    motor = the_board.set_pin_mode_stepper(interface=2, pin1=PULSE_PIN,
                                                 pin2=DIRECTION_PIN)

    # if you are using a 28BYJ-48 Stepper Motor with ULN2003
    # comment out the line above and uncomment out the line below.
    # motor = await the_board.set_pin_mode_stepper(interface=4, pin1=5, pin2=4, pin3=14,
    # pin4=12)

    # set the max speed and speed
    the_board.stepper_set_max_speed(motor, 900)
    the_board.stepper_set_speed(motor, 800)
    # run the motor
    the_board.stepper_run_speed(motor)

    # keep application running
    while True:
        try:
            time.sleep(.0002)
        except KeyboardInterrupt:
            the_board.shutdown()
            sys.exit(0)


# instantiate telemetrix
board = telemetrix_esp32.TelemetrixEsp32(transport_is_wifi=False)

try:
    # start the main function
    step_continuous(board)
    board.shutdown()

except KeyboardInterrupt:
    board.shutdown()
