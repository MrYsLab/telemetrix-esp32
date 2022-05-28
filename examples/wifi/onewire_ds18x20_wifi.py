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

"""
This example demonstrates OneWire operations by reading a  
DS18B20 or DS1822 temperature sensor.
"""

# IP address assigned to the ESP32
IP_ADDRESS = '192.168.2.232'

# GPIO pin attached to OneWire signal
ONE_WIRE_PIN = 23

import sys
import time
from telemetrix_esp32 import telemetrix_esp32


# noinspection PyArgumentList
class OneWireTemp:
    """
    This class implements reading the sensor
    """

    def __init__(self, my_board, pin):
        """

        :param pin: data pin connected to the device
        """
        self.pin = pin
        self.board = my_board

        # a dictionary to determine the device type
        self.chip_types = {0x10: 'DS18S20', 0x28: 'DS18B20', 0x22: 'DS1822'}

        # callback distributor map
        # use the callback type to call the appropriate processing method
        self.callback_distribution = {34: self.search_cb, 35: self.crc_cb,
                                      28: self.reset_cb,
                                      32: self.read_cb}

        # a list to hold the detected device address
        self.address = []

        # a list to hold the measured temperature returned from device
        self.temperature_data = []

        # crc calculation result
        self.crc_comparator = None

    def run_it(self):
        """
        Access the device and print the results
        """

        # initialize OneWire operation for the pin
        try:
            self.board.set_pin_mode_one_wire(self.pin)

            # find the devices address
            self.board.onewire_search(self.onewire_callback)
            time.sleep(1)

            if not self.address:
                print('Did not receive address')
                self.board.shutdown()
                sys.exit(0)

            # check crc of the address
            # the callback does the actual compare
            self.board.onewire_crc8(list(self.address), self.onewire_callback)
            time.sleep(.3)

            # identify and print the chip type based on the address
            chip_type = self.chip_types[self.address[0]]
            print(f'Chip detected: {chip_type}\n')
            if chip_type == 'DS18S20':
                print('This application does not support the DS18S20')
                self.board.shutdown()
                sys.exit(0)
        except Exception:
            self.board.shutdown()
            sys.exit(0)

        # reset the device, select the device and do a temperature
        # conversion
        while True:
            try:
                self.board.onewire_reset(callback=self.onewire_callback)

                # here we use skip instead of using select
                self.board.onewire_skip()

                # do a temperature conversion
                self.board.onewire_write(0x44, 1)

                # allow 1 second for the conversion to complete
                time.sleep(1)

                # reset
                self.board.onewire_reset(callback=self.onewire_callback)

                self.board.onewire_skip()

                # read  the data from the scratch pad
                self.board.onewire_write(0xBE)

                for x in range(10):
                    self.board.onewire_read(self.onewire_callback)

                time.sleep(1)

                # the temperature is contained in the first two bytes of the data
                raw = (self.temperature_data[1] << 8) | self.temperature_data[0]
                celsius = raw / 16.0
                print("Celsius = {:0.2f}º C.".format(celsius))
                fahrenheit = celsius * 1.8 + 32.0
                print("Fahrenheit = {:0.2f}º F.".format(fahrenheit))
                # clear out the buffer for the next read
                self.temperature_data = []
                print()
            except KeyboardInterrupt:
                self.board.shutdown()
                sys.exit(0)

    def onewire_callback(self, report):
        # This is the main callback distributor.
        # Call the specific handler to service the callback
        # subtype.

        # Report format: [ReportType = 14, Report Subtype, Report Data..., timestamp]

        if report[1] not in self.callback_distribution:
            return  # ignore unknown types
        else:
            self.callback_distribution[report[1]](report)

    def search_cb(self, report):
        """
        Search report handler

        :param report: [ReportType = 14, Report Subtype = 31, 8 bytes of device address,
                        timestamp]
        """
        self.address = [report[x] for x in range(2, 10)]
        print('Device Address = ', " ", end="")
        for data in self.address:
            print(hex(data), " ", end="")
        print()
        self.crc_comparator = report[9]

    def crc_cb(self, report):
        """
        Crc result handler
        :param report: [ReportType = 14, Report Subtype = 21, calculated CRC byte,
                        timestamp]
        :return:
        """
        # print(f'CRC = {hex(report[2])}')
        if report[2] != self.crc_comparator:
            print('CRC Is Invalid')
            self.board.shutdown()
            sys.exit(0)

    def reset_cb(self, report):
        """
        Reset callback
        :param report: [ReportType = 14, Report Subtype = 25, reset result byte,
                        timestamp]
        """
        # not used - just ignore it
        pass

    def read_cb(self, report):
        """
        Byte read callback handler
        Append each byte received to the temperature data list
        When 9 bytes are received, check the data's CRC.

        :param report: [ReportType = 14, Report Subtype = 29, 9 temperature bytes,
                        timestamp]

        """
        self.temperature_data.append(report[2])
        if len(self.temperature_data) == 9:
            self.board.onewire_crc8(self.temperature_data,
                                          callback=self.onewire_callback)
            # hex_list = [hex(x) for x in self.temperature_data]
            # print(hex_list)
            self.crc_comparator = self.temperature_data[-1:][0]


def onewire_example(the_board, data_pin):
    """
    Set the pin mode for a onewire device. Results will appear via the
    callback.

    :param the_board: telemetrix aio instance
    :param data_pin: GPIO pin number
    """

    owt = OneWireTemp(the_board, data_pin)
    owt.run_it()
    # wait forever
    while True:
        try:
            time.sleep(.01)
        except KeyboardInterrupt:
            the_board.shutdown()
            sys.exit(0)


# instantiate telemetrix
board = telemetrix_esp32.TelemetrixEsp32(transport_address=IP_ADDRESS)

try:
    # start the main function
    onewire_example(board, ONE_WIRE_PIN)
    board.shutdown()
    sys.exit(0)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
