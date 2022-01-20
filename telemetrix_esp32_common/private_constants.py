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


class PrivateConstants:
    """
    This class contains a set of constants for telemetrix internal use .
    """

    # commands
    # send a loop back request - for debugging communications
    LOOP_COMMAND = 0
    SET_PIN_MODE = 1  # set a pin to INPUT/OUTPUT/PWM/etc
    DIGITAL_WRITE = 2  # set a single digital pin value instead of entire port
    ANALOG_WRITE = 3
    MODIFY_REPORTING = 4
    GET_FIRMWARE_VERSION = 5
    SERVO_ATTACH = 6
    SERVO_WRITE = 7
    SERVO_DETACH = 8
    I2C_BEGIN = 9
    I2C_READ = 10
    I2C_WRITE = 11
    SONAR_NEW = 12
    DHT_NEW = 13
    STOP_ALL_REPORTS = 14
    SET_ANALOG_SCANNING_INTERVAL = 15
    ENABLE_ALL_REPORTS = 16
    ANALOG_OUT_ATTACH = 17
    ANALOG_OUT_DETACH = 18
    DAC_WRITE = 19
    RESET = 20
    DAC_DISABLE = 21
    SPI_INIT = 22
    SPI_WRITE_BLOCKING = 23
    SPI_READ_BLOCKING = 24
    SPI_SET_FORMAT = 25
    SPI_CS_CONTROL = 26
    ONE_WIRE_INIT = 27
    ONE_WIRE_RESET = 28
    ONE_WIRE_SELECT = 29
    ONE_WIRE_SKIP = 30
    ONE_WIRE_WRITE = 31
    ONE_WIRE_READ = 32
    ONE_WIRE_RESET_SEARCH = 33
    ONE_WIRE_SEARCH = 34
    ONE_WIRE_CRC8 = 35
    SET_PIN_MODE_STEPPER = 36
    STEPPER_MOVE_TO = 37
    STEPPER_MOVE = 38
    STEPPER_RUN = 39
    STEPPER_RUN_SPEED = 40
    STEPPER_SET_MAX_SPEED = 41
    STEPPER_SET_ACCELERATION = 42
    STEPPER_SET_SPEED = 43
    STEPPER_SET_CURRENT_POSITION = 44
    STEPPER_RUN_SPEED_TO_POSITION = 45
    STEPPER_STOP = 46
    STEPPER_DISABLE_OUTPUTS = 47
    STEPPER_ENABLE_OUTPUTS = 48
    STEPPER_SET_MINIMUM_PULSE_WIDTH = 49
    STEPPER_SET_ENABLE_PIN = 50
    STEPPER_SET_3_PINS_INVERTED = 51
    STEPPER_SET_4_PINS_INVERTED = 52
    STEPPER_IS_RUNNING = 53
    STEPPER_GET_CURRENT_POSITION = 54
    STEPPER_GET_DISTANCE_TO_GO = 55
    STEPPER_GET_TARGET_POSITION = 56

    # reports
    # debug data from server = 0
    DIGITAL_REPORT = DIGITAL_WRITE
    ANALOG_REPORT = ANALOG_WRITE
    FIRMWARE_REPORT = GET_FIRMWARE_VERSION
    SERVO_UNAVAILABLE = SERVO_ATTACH
    I2C_TOO_FEW_BYTES_RCVD = 7
    I2C_TOO_MANY_BYTES_RCVD = 8
    I2C_READ_REPORT = 9
    SONAR_DISTANCE = 10
    DHT_REPORT = 11
    TOUCH_REPORT = 12
    SPI_REPORT = 13
    ONE_WIRE_REPORT = 14
    STEPPER_DISTANCE_TO_GO = 15
    STEPPER_TARGET_POSITION = 16
    STEPPER_CURRENT_POSITION = 17
    STEPPER_RUNNING_REPORT = 18
    STEPPER_RUN_COMPLETE_REPORT = 19

    DEBUG_PRINT = 99

    TELEMETRIX_ESP32_VERSION = "1.0"
    TELEMETRIX_AIO_ESP32_VERSION = "1.0"

    # reporting control
    REPORTING_DISABLE_ALL = 0
    REPORTING_ANALOG_ENABLE = 1
    REPORTING_DIGITAL_ENABLE = 2
    REPORTING_ANALOG_DISABLE = 3
    REPORTING_DIGITAL_DISABLE = 4

    # Pin mode definitions
    AT_INPUT = 0
    AT_OUTPUT = 1
    AT_INPUT_PULLUP = 2
    AT_ANALOG = 3
    AT_SERVO = 4
    AT_SONAR = 5
    AT_DHT = 6
    AT_TOUCH = 7
    AT_PWM_OUT = 8
    AT_INPUT_PULL_DOWN = 9
    AT_MODE_NOT_SET = 255

    # maximum number of digital pins supported
    NUMBER_OF_DIGITAL_PINS = 100

    # maximum number of analog pins supported
    NUMBER_OF_ANALOG_PINS = 20

    # maximum number of sonars allowed
    MAX_SONARS = 6

    # maximum number of DHT devices allowed
    MAX_DHTS = 6

    # DHT Report subtypes
    DHT_DATA = 0
    DHT_ERROR = 1
