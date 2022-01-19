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
import struct
import sys
import time

# noinspection PyUnresolvedReferences
from telemetrix_esp32_common.private_constants import PrivateConstants


class TelemetrixAioEsp32:
    """
    This class exposes and implements the TelemetrixAIO API for the ESP32 using
    a BLE transport.
    It includes the public API methods as well as
    a set of private methods. This is an asyncio API.

    """

    # noinspection PyPep8,PyPep8
    def __init__(self, transport_is_ble=True, transport_address=None,
                 ip_port=31336, autostart=True,
                 loop=None, shutdown_on_exception=True,
                 restart_on_shutdown=True,
                 ):

        """
        The "constructor" method.

        :param transport_is_ble: True if BLE or False if WI-FI

        :param transport_address: mac address for BLE or IP address for WI-FI

        :param ip_port: if using a WI-FI interface, this specifies the IP port number

        :param autostart: If you wish to call the start method within
                          your application, then set this to False.

        :param loop: optional user provided event loop

        :param shutdown_on_exception: call shutdown before raising
                                      a RunTimeError exception, or
                                      receiving a KeyboardInterrupt exception

        :param restart_on_shutdown: restart the esp32 processor upon shutdown



        """

        # check to make sure that Python interpreter is version 3.8.3 or greater
        python_version = sys.version_info
        if python_version[0] >= 3:
            if python_version[1] >= 7:
                if python_version[2] >= 0:
                    pass
            else:
                raise RuntimeError("ERROR: Python 3.7.0 or greater is "
                                   "required for use of this program.")

        # save input parameters

        self.transport_is_ble = transport_is_ble

        self.ip_port = ip_port

        self.autostart = autostart

        # set the event loop
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.transport = None

        # sender id  when BLE data is received
        # not currently used
        self.sender = None

        self.transport_address = transport_address
        self.shutdown_on_exception = shutdown_on_exception
        self.restart_on_shutdown = restart_on_shutdown

        # dictionaries to store the callbacks for each pin
        self.analog_callbacks = {}

        self.digital_callbacks = {}

        self.i2c_callback = None

        self.i2c_active = False

        self.spi_callback = None

        self.onewire_callback = None

        self.cs_pins_enabled = []

        # flag to indicate if spi is initialized
        self.spi_enabled = False

        # flag to indicate if onewire is initialized
        self.onewire_enabled = False

        # debug loopback callback method
        self.loop_back_callback = None

        # the trigger pin will be the key to retrieve
        # the callback for a specific HC-SR04
        self.sonar_callbacks = {}

        self.sonar_count = 0

        self.dht_callbacks = {}

        self.dht_count = 0

        self.touch_callbacks = {}

        # flag to indicate we are in shutdown mode
        self.shutdown_flag = False

        self.report_buffer = []

        self.report_dispatch = {}

        self.the_task = None

        self.firmware_version = None

        # To add a command to the report dispatch table, append here.
        self.report_dispatch.update(
            {PrivateConstants.LOOP_COMMAND: self._report_loop_data})
        self.report_dispatch.update(
            {PrivateConstants.DEBUG_PRINT: self._report_debug_data})
        self.report_dispatch.update(
            {PrivateConstants.DIGITAL_REPORT: self._digital_message})
        self.report_dispatch.update(
            {PrivateConstants.ANALOG_REPORT: self._analog_message})
        self.report_dispatch.update(
            {PrivateConstants.SERVO_UNAVAILABLE: self._servo_unavailable})
        self.report_dispatch.update(
            {PrivateConstants.I2C_READ_REPORT: self._i2c_read_report})
        self.report_dispatch.update(
            {PrivateConstants.I2C_TOO_FEW_BYTES_RCVD: self._i2c_too_few})
        self.report_dispatch.update(
            {PrivateConstants.I2C_TOO_MANY_BYTES_RCVD: self._i2c_too_many})
        self.report_dispatch.update(
            {PrivateConstants.SONAR_DISTANCE: self._sonar_distance_report})
        self.report_dispatch.update({PrivateConstants.DHT_REPORT: self._dht_report})
        self.report_dispatch.update({PrivateConstants.FIRMWARE_REPORT:
                                         self._firmware_report})
        self.report_dispatch.update({PrivateConstants.TOUCH_REPORT: self._touch_report})
        self.report_dispatch.update(
            {PrivateConstants.ONE_WIRE_REPORT: self._onewire_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_DISTANCE_TO_GO:
                 self._stepper_distance_to_go_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_TARGET_POSITION:
                 self._stepper_target_position_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_CURRENT_POSITION:
                 self._stepper_current_position_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_RUNNING_REPORT:
                 self._stepper_is_running_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_RUN_COMPLETE_REPORT:
                 self._stepper_run_complete_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_DISTANCE_TO_GO:
                 self._stepper_distance_to_go_report})
        self.report_dispatch.update(
            {PrivateConstants.STEPPER_TARGET_POSITION:
                 self._stepper_target_position_report})
        self.report_dispatch.update(
            {PrivateConstants.SPI_REPORT: self._spi_report})

        # valid pin numbers
        self.valid_gpio_input_pins = [4, 5, 12, 13, 14, 16, 17, 18, 19, 21,
                                      22, 23, 25, 26, 27, 32, 33]

        self.valid_gpio_output_pins = [2, 4, 5, 12, 13, 14, 16, 17, 18, 19, 21,
                                       22, 23, 25, 26, 27, 32, 33]

        self.valid_touch_pins = [4, 12, 13, 14, 15, 27, 32, 33]

        self.valid_analog_in_pins = [32, 33, 34, 35, 36, 39]

        self.valid_servo_pins = [4, 5, 12, 13, 14, 16, 17, 18, 19, 21,
                                 22, 23, 25, 26, 27, 32, 33]
        # updated when a new motor is added
        self.next_stepper_assigned = 0

        # valid list of stepper motor interface types
        self.valid_stepper_interfaces = [1, 2, 3, 4, 6, 8]

        # maximum number of steppers supported
        self.max_number_of_steppers = 4

        # number of steppers created - not to exceed the maximum
        self.number_of_steppers = 0

        # dictionary to hold stepper motor information
        self.stepper_info = {'instance': False, 'is_running': None,
                             'maximum_speed': 1, 'speed': 0, 'acceleration': 0,
                             'distance_to_go_callback': None,
                             'target_position_callback': None,
                             'current_position_callback': None,
                             'is_running_callback': None,
                             'motion_complete_callback': None,
                             'acceleration_callback': None}

        # build a list of stepper motor info items
        self.stepper_info_list = []
        # a list of dictionaries to hold stepper information
        for motor in range(self.max_number_of_steppers):
            self.stepper_info_list.append(self.stepper_info)

        print(
            f'TelemetrixAioEsp32 Version: {PrivateConstants.TELEMETRIX_AIO_ESP32_VERSION}')
        print(f'Copyright (c) 2022 Alan Yorinks All rights reserved.\n')

        if autostart:
            self.loop.run_until_complete(self.start_aio())

    async def start_aio(self):
        """
        This method may be called directly, if the autostart
        parameter in __init__ is set to false.

        This method instantiates the BLE transport interface

        Use this method if you wish to start TelemetrixAIO manually from
        an asyncio function.
         """

        if self.transport_is_ble:
            from telemetrix_esp32_common.ble_transport import BleTransport
            self.transport = BleTransport(receive_callback=self._ble_report_dispatcher)
            await self.transport.connect()
        else:
            from telemetrix_esp32_common.aio_socket_transport import AioSocketTransport

            self.transport = AioSocketTransport(self.transport_address, self.ip_port,
                                                self.loop)
            await self.transport.start()
            self.the_task = self.loop.create_task(self._wifi_report_dispatcher())

        await self._get_firmware_version()

        if not self.firmware_version:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('Could not retrieve server firmware version')

        if self.transport_is_ble:
            print(f'Telemetrix4Esp32BLE Firmware Version: {self.firmware_version[0]}'
                f'.{self.firmware_version[1]}.{self.firmware_version[2]}')

        else:
            print(f'Telemetrix4Esp32WIFI Firmware Version: {self.firmware_version[0]}'
                  f'.{self.firmware_version[1]}.{self.firmware_version[2]}')
        command = [PrivateConstants.ENABLE_ALL_REPORTS]

        await self._send_command(command)

    async def get_event_loop(self):
        """
        Return the currently active asyncio event loop

        :return: Active event loop

        """
        return self.loop

    async def _get_firmware_version(self):
        """
        This method retrieves the Telemetrix4Esp32BLE firmware version

        :returns: Firmata firmware version
        """
        command = [PrivateConstants.GET_FIRMWARE_VERSION]
        await self._send_command(command)
        # provide time for the reply
        await asyncio.sleep(.2)

    async def analog_write(self, channel, value):
        """
        Set the specified pin to the specified value.

        :param channel: pwm channel number established in set_pin_mode_analog_output

        :param value: pin value (maximum 16 bits)

        """
        value_msb = value >> 8
        value_lsb = value & 0xff
        command = [PrivateConstants.ANALOG_WRITE, channel, value_msb, value_lsb]
        await self._send_command(command)

    async def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: GPIO pin number

        :param value: pin value (1 or 0)

        """
        command = [PrivateConstants.DIGITAL_WRITE, pin, value]
        await self._send_command(command)

    async def i2c_read(self, address, register, number_of_bytes,
                       callback):
        """
        Read the specified number of bytes from the specified register for
        the i2c device.


        :param address: i2c device address

        :param register: i2c register (or None if no register selection is needed)

        :param number_of_bytes: number of bytes to be read

        :param callback: Required callback function to report i2c data as a
                   result of read command

        callback returns a data list:

        [I2C_READ_REPORT, address, register, count of data bytes, data bytes, time-stamp]

        """
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('i2c_read: A Callback must be specified')

        await self._i2c_read_request(address, register, number_of_bytes,
                                     callback=callback)

    async def i2c_read_restart_transmission(self, address, register,
                                            number_of_bytes,
                                            callback):
        """
        Read the specified number of bytes from the specified register for
        the i2c device. This restarts the transmission after the read. It is
        required for some i2c devices such as the MMA8452Q accelerometer.


        :param address: i2c device address

        :param register: i2c register (or None if no register
                                                    selection is needed)

        :param number_of_bytes: number of bytes to be read

        :param callback: Required callback function to report i2c data as a
                   result of read command

        callback returns a data list:

        [I2C_READ_REPORT, address, register, count of data bytes, data bytes, time-stamp]

        """
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'i2c_read_restart_transmission: A Callback must be specified')

        await self._i2c_read_request(address, register, number_of_bytes,
                                     stop_transmission=False,
                                     callback=callback)

    async def _i2c_read_request(self, address, register, number_of_bytes,
                                stop_transmission=True, callback=None):
        """
        This method requests the read of an i2c device. Results are retrieved
        via callback.

        :param address: i2c device address

        :param register: register number (or None if no register selection is needed)

        :param number_of_bytes: number of bytes expected to be returned

        :param stop_transmission: stop transmission after read

        :param callback: Required callback function to report i2c data as a
                   result of read command.

        """
        if not self.i2c_active:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'I2C Read: set_pin_mode i2c never called.')

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('I2C Read: A callback function must be specified.')

        self.i2c_callback = callback

        if not register:
            register = 0

        # message contains:
        # 1. address
        # 2. register
        # 3. number of bytes
        # 4. restart_transmission - True or False
        # 5. i2c port

        command = [PrivateConstants.I2C_READ, address, register, number_of_bytes,
                   stop_transmission]
        await self._send_command(command)

    async def i2c_write(self, address, args):
        """
        Write data to an i2c device.

        :param address: i2c device address

        :param args: A variable number of bytes to be sent to the device
                     passed in as a list

        """
        if not self.i2c_active:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'I2C Write: set_pin_mode i2c never called for i2c port 1.')

        command = [PrivateConstants.I2C_WRITE, len(args), address]

        for item in args:
            command.append(item)

        await self._send_command(command)

    async def loop_back(self, start_character, callback=None):
        """
        This is a debugging method to send a character to the
        ESP32, and have the device loop it back.

        :param start_character: The character to loop back. It should be
                                an integer.

        :param callback: Looped back character will appear in the callback method

        """

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('loop_back: A callback function must be specified.')
        command = [PrivateConstants.LOOP_COMMAND, ord(start_character)]

        self.loop_back_callback = callback
        await self._send_command(command)

    async def set_analog_scan_interval(self, interval):
        """
        Set the analog scanning interval.

        :param interval: value of 0 - 255 - milliseconds
        """

        if 0 <= interval <= 255:
            command = [PrivateConstants.SET_ANALOG_SCANNING_INTERVAL, interval]
            await self._send_command(command)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('Analog interval must be between 0 and 255')

    async def set_pin_mode_analog_input(self, pin_number, differential=0, callback=None):
        """
        Set a pin as an analog input.

        :param pin_number: GPIO pin number

       valid pins:

           32, 33, 34, 35, 36, 39

        :param differential: difference in previous to current value before
                             report will be generated

        :param callback: async callback function

        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for analog input pins = 2

        """

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'set_pin_mode_analog_input: A callback function must be specified.')

        if pin_number in self.valid_analog_in_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_ANALOG,
                                     differential, callback=callback)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_digital_input: Invalid GPIO pin number')

    async def set_pin_mode_analog_output(self, pin_number, channel=0, frequency=5000.0,
                                         resolution=8):
        """
        Set a pin as a pwm (analog output) pin. This method attaches the pin
        to a channel as well as specifying the channel parameters.

        The pwm_attach is done automatically on the server.

        :param pin_number: valid output GPIO pin number

       valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param channel: PWM channel (0 -15)

        :param frequency: floating point signal frequency (10Hz - 300kHz)

        :param resolution: number of bits of resolution (81-16)

        """
        # check if the pin number is a valid gpio output pin
        if pin_number in self.valid_gpio_output_pins:
            if 0 <= channel < 16:
                if 10.0 < frequency < 300000.0:
                    if 1 < resolution < 16:
                        # all is valid - create the message
                        command = [PrivateConstants.SET_PIN_MODE, pin_number,
                                   PrivateConstants.AT_PWM_OUT, channel, resolution]
                        # convert and insert the 8 frequency bytes into the message.
                        freq_array = bytearray(struct.pack("d", frequency))
                        for value in freq_array:
                            command.append(value)
                        await self._send_command(command)
                    else:
                        if self.shutdown_on_exception:
                            await self.shutdown()
                        raise RuntimeError(
                            "set_pin_mode_analog_out: Valid resolution range 8 - 16.")

                else:
                    if self.shutdown_on_exception:
                        await self.shutdown()
                    raise RuntimeError(
                        "set_pin_mode_analog_out: Valid frequency range 10.0 - 300000.0.")

            else:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError("set_pin_mode_analog_out: Valid channel range 0-15.")

        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError("set_pin_mode_analog_out:  select a valid gpio pin number")

    async def attach_pin_to_analog_channel(self, pin_number, channel):
        """
        If the pin number is a valid pin and the channel was initialized,
        attach the specified pin.

        The pwm_attach is initially done on the server side as a result of calling
        set_pin_mode_analog_output. This method is provided if you with to manually
        do a pwm_attach.

        :param pin_number: GPIO pin Number

        :param channel:  PWM Channel Number (0-15)
        """

        # check to see if the pin is a valid pin number
        if pin_number in self.valid_gpio_output_pins:
            # check to see if the channel is in range
            if 0 <= channel < 16:
                command = [PrivateConstants.ANALOG_OUT_ATTACH, pin_number, channel]
                await self._send_command(command)
            else:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError(
                    'attach_pin_to_analog_channel: Invalid channel number.')
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('attach_pin_to_analog_channel: Invalid GPIO pin number')

    async def detach_pin_to_analog_channel(self, pin_number, channel):
        """
        If the pin number is a valid pin and the channel was initialized, detach the specified pin.

        This method is provided if you with to manually detach a pin from a pwm
        channel.

        :param pin_number: GPIO pin number

        :param channel:  PWM Channel Number (0 -15)
        """

        # check to see if the pin is a valid pin number
        if pin_number in self.valid_gpio_output_pins:
            # check to see if the channel is in range
            if 0 <= channel < 16:
                command = [PrivateConstants.ANALOG_OUT_DETACH, pin_number, channel]
                await self._send_command(command)
            else:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError('detach_pin_to_analog_channel: Invalid channel '
                                   'number')
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('detach_pin_to_analog_channel: Invalid GPIO pin number')

    async def set_pin_mode_dac(self, pin_number, value):
        """
        This method sets a dac pin (GPIO 25 = dac1, GPIO 26 = dac2) to the specified
        value.

        :param pin_number: 25 or 26

        :param value: 0 - 255 (255= 3.3V 128=1.65V)
        """

        if pin_number == 25 or pin_number == 26:
            if 0 <= value <= 255:
                command = [PrivateConstants.DAC_WRITE, pin_number, value]
                await self._send_command(command)
            else:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError('set_pin_mode_dac: Invalid value')
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_dac: Invalid GPIO pin number')

    async def dac_disable(self, pin_number):
        """
        Disable DAC mode for the specified pin.

        :param pin_number: GPIO 25 or 26
        """

        if pin_number == 25 or pin_number == 26:
            command = [PrivateConstants.DAC_DISABLE, pin_number]
            await self._send_command(command)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('dac_disable: Invalid pin number')

    async def set_pin_mode_digital_input(self, pin_number, callback):
        """
        Set a pin as a digital input.

        :param pin_number: GPIO pin number.

       Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param callback: async callback function

        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins = 2

        """
        if pin_number in self.valid_gpio_output_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_INPUT,
                                     differential=0, callback=callback)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_digital_input: Invalid GPIO pin number')

    async def set_pin_mode_digital_input_pulldown(self, pin_number, callback):
        """
        Set a pin as a digital input with pulldown enabled.

        :param pin_number: GPIO pin number.

       Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param callback: async callback function

        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins with pull_downs enabled = 2

        """
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'set_pin_mode_digital_input_pulldown: A callback function must be '
                'specified.')

        if pin_number in self.valid_gpio_input_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_INPUT_PULL_DOWN,
                                     differential=0, callback=callback)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'set_pin_mode_digital_input_pulldown: Invalid GPIO pin number')

    async def set_pin_mode_digital_input_pullup(self, pin_number, callback):
        """
        Set a pin as a digital input with pullup enabled.

        :param pin_number: GPIO pin number

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param callback: async callback function

        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins with pullups enabled = 2

        """
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'set_pin_mode_digital_input_pullup: A callback function must be specified.')

        if pin_number in self.valid_gpio_input_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_INPUT_PULLUP,
                                     differential=0, callback=callback)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'set_pin_mode_digital_input_pullup: Invalid GPIO pin number')

    async def set_pin_mode_digital_output(self, pin_number):
        """
        Set a pin as a digital output pin.

        :param pin_number: GPIO pin number.

       Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33
        """

        if pin_number in self.valid_gpio_output_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_OUTPUT,
                                     differential=0, callback=None)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_digital_output: Invalid GPIO pin number')

    # noinspection PyIncorrectDocstring
    async def set_pin_mode_i2c(self):
        """
        Establish the standard ESP32 i2c pins for i2c utilization.

        SDA = GPIO 21    SDC = GPIO 22

        NOTES:

             1. THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE

             2. Callbacks are set within the individual i2c read methods of this
              API.

              See i2c_read, or i2c_read_restart_transmission.

        """
        # if not previously activated set it to activated
        # and then send a "begin" message for this port
        if not self.i2c_active:
            self.i2c_active = True
        else:
            return

        command = [PrivateConstants.I2C_BEGIN]
        await self._send_command(command)

    async def set_pin_mode_dht(self, pin_number, callback):
        """

        :param pin_number: connection pin.

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param callback: callback function

        """

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_dht: A Callback must be specified')

        if pin_number in self.valid_gpio_input_pins:
            if self.dht_count < PrivateConstants.MAX_DHTS - 1:
                self.dht_callbacks[pin_number] = callback
                self.dht_count += 1

                command = [PrivateConstants.DHT_NEW, pin_number]
                await self._send_command(command)
            else:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError(
                    f'Maximum Number Of DHTs Exceeded - set_pin_mode_dht fails for pin {pin_number}')
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_dht: Invalid GPIO pin number')

    # noinspection PyRedundantParentheses
    async def set_pin_mode_servo(self, pin_number, min_pulse=544, max_pulse=2400):
        """

        Attach a pin to a servo motor

        :param pin_number: GPIO pin.

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33


        :param min_pulse: minimum pulse width

        :param max_pulse: maximum pulse width

        """
        if pin_number in self.valid_servo_pins:
            minv = (min_pulse).to_bytes(2, byteorder="big")
            maxv = (max_pulse).to_bytes(2, byteorder="big")

            command = [PrivateConstants.SERVO_ATTACH, pin_number,
                       minv[0], minv[1], maxv[0], maxv[1]]
            await self._send_command(command)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_servo: Invalid GPIO pin number')

    async def set_pin_mode_sonar(self, trigger_pin, echo_pin,
                                 callback):
        """
        Attach pins to a servo device. Trigger and echo pins must not be the same value.

        :param trigger_pin:

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param echo_pin:

        :param callback:  callback

        """

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_sonar: A Callback must be specified')

        if trigger_pin in self.valid_gpio_input_pins:
            if echo_pin in self.valid_gpio_input_pins:
                if self.sonar_count < PrivateConstants.MAX_SONARS - 1:
                    self.sonar_callbacks[trigger_pin] = callback
                    self.sonar_count += 1

                    command = [PrivateConstants.SONAR_NEW, trigger_pin, echo_pin]
                    await self._send_command(command)
                else:
                    if self.shutdown_on_exception:
                        await self.shutdown()
                    raise RuntimeError(
                        f'Maximum Number Of Sonars Exceeded - set_pin_mode_sonar fails for pin {trigger_pin}')
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_sonar: Invalid GPIO pin number')

    async def set_pin_mode_spi(self, chip_select_list=None):
        """
        Specify the list of chip select pins.

        Standard ESP32 MISO, MOSI and CLK pins are used for the board in use.
        SPI GPIO Pins For the ESP32:

        CS    = 5

        MOSI  = 23

        MISO  = 19

        SCK   = 18

        Chip Select is any digital output capable pin.

        :param chip_select_list: this is a list of pins to be used for chip select.
                           The pins will be configured as output, and set to high
                           ready to be used for chip select.
                           NOTE: You must specify the chips select pins here!

        Valid CS pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33
        """

        if type(chip_select_list) != list:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('chip_select_list must be in the form of a list')
        if not chip_select_list:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('Chip select pins were not specified')

        self.spi_enabled = True

        command = [PrivateConstants.SPI_INIT, len(chip_select_list)]

        for pin in chip_select_list:
            command.append(pin)
            self.cs_pins_enabled.append(pin)
        await self._send_command(command)

    async def set_pin_mode_touch(self, pin_number, differential=0, callback=None):
        """
        Set a pin to touch mode

        :param pin_number:  GPIO pin number.

        Valid pins:

           4, 12, 13, 14, 15, 27, 32, 33

        :param differential: difference in previous to current value before
                             report will be generated

        :param callback: callback function


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for touch pins = 13

        """
        if pin_number in self.valid_touch_pins:
            await self._set_pin_mode(pin_number, PrivateConstants.AT_TOUCH, differential,
                                     callback)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('set_pin_mode_touch: Invalid GPIO pin number')

    async def _set_pin_mode(self, pin_number, pin_state, differential, callback):
        """
        A private method to set the various pin modes.

        :param pin_number: GPIO pin number

        :param pin_state: INPUT/OUTPUT/ANALOG/PWM/PULLUP - for SERVO use
                          servo_config()
                          For DHT   use: set_pin_mode_dht

       :param differential: for analog inputs - threshold
                             value to be achieved for report to
                             be generated

        :param callback: A reference to an async call back function to be
                         called when pin data value changes

        """
        if not callback and pin_state != PrivateConstants.AT_OUTPUT:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('_set_pin_mode: A Callback must be specified')
        else:
            if pin_state == PrivateConstants.AT_INPUT:
                self.digital_callbacks[pin_number] = callback
            elif pin_state == PrivateConstants.AT_INPUT_PULLUP:
                self.digital_callbacks[pin_number] = callback
            elif pin_state == PrivateConstants.AT_INPUT_PULL_DOWN:
                self.digital_callbacks[pin_number] = callback
            elif pin_state == PrivateConstants.AT_ANALOG:
                self.analog_callbacks[pin_number] = callback
            elif pin_state == PrivateConstants.AT_TOUCH:
                self.touch_callbacks[pin_number] = callback

        if pin_state == PrivateConstants.AT_INPUT:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_INPUT, 1]

        elif pin_state == PrivateConstants.AT_INPUT_PULLUP:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_INPUT_PULLUP, 1]

        elif pin_state == PrivateConstants.AT_INPUT_PULL_DOWN:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_INPUT_PULL_DOWN, 1]

        elif pin_state == PrivateConstants.AT_OUTPUT:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_OUTPUT]

        elif pin_state == PrivateConstants.AT_ANALOG:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_ANALOG,
                       differential >> 8, differential & 0xff, 1]
        elif pin_state == PrivateConstants.AT_TOUCH:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_TOUCH,
                       differential >> 8, differential & 0xff, 1]

        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('Unknown pin state')

        if command:
            await self._send_command(command)

        # await asyncio.sleep(.05)

    async def set_pin_mode_stepper(self, interface=4, pin1=2, pin2=3, pin3=4,
                                   pin4=5, enable=True):
        """
        Stepper motor support is implemented as a proxy for
        the AccelStepper library for the ESP32.

        https://github.com/waspinator/AccelStepper

        Instantiate a stepper motor.

        Initialize the interface and pins for a stepper motor.

        Valid GPIO pin numbers:

                    2, 4, 5, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                    24, 25, 26, 27, 28., 29, 30, 31, 32, 33, 34, 35, 36,
                    37, 38, 39

        :param interface: Motor Interface Type:

                1 = Stepper Driver, 2 driver pins required

                2 = FULL2WIRE  2 wire stepper, 2 motor pins required

                3 = FULL3WIRE 3 wire stepper, such as HDD spindle,
                    3 motor pins required

                4 = FULL4WIRE, 4 wire full stepper, 4 motor pins
                    required

                6 = HALF3WIRE, 3 wire half stepper, such as HDD spindle,
                    3 motor pins required

                8 = HALF4WIRE, 4 wire half stepper, 4 motor pins required

        :param pin1: GPIO digital pin number for motor pin 1

        :param pin2: GPIO digital pin number for motor pin 2

        :param pin3: GPIO digital pin number for motor pin 3

        :param pin4: GPIO digital pin number for motor pin 4

        :param enable: If this is true, the output pins at construction time.

        :return: Motor Reference number
        """
        if pin1 in self.valid_gpio_input_pins and pin2 in self.valid_gpio_input_pins \
                and pin3 in self.valid_gpio_input_pins and pin4 in \
                self.valid_gpio_input_pins:

            if self.number_of_steppers == self.max_number_of_steppers:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError('Maximum number of steppers has already been assigned')

            if interface not in self.valid_stepper_interfaces:
                if self.shutdown_on_exception:
                    await self.shutdown()
                raise RuntimeError('Invalid stepper interface')

            self.number_of_steppers += 1

            motor_id = self.next_stepper_assigned
            self.next_stepper_assigned += 1
            self.stepper_info_list[motor_id]['instance'] = True

            # build message and send message to server
            command = [PrivateConstants.SET_PIN_MODE_STEPPER, motor_id, interface, pin1,
                       pin2, pin3, pin4, enable]
            await self._send_command(command)

            # return motor id
            return motor_id
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'One or more GPIO pins are incorrect')

    async def stepper_move_to(self, motor_id, position):
        """
        Set an absolution target position. If position is positive, the movement is
        clockwise, else it is counter-clockwise.

        The stepper_run function will try to move the motor (at most one step per
        call)
        from the current position to the target position set by the most
        recent call to this function. Caution: moveTo() also recalculates the
        speed for the next step.
        If you are trying to use constant speed movements, you should call setSpeed()
        after calling moveTo().

        :param motor_id: motor id: 0 - 3

        :param position: target position. Maximum value is 32 bits.
        """

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_move_to: Invalid motor_id.')

        polarity = 0

        if position < 0:
            polarity = 1
            position = abs(position)

        position_bytes = list(position.to_bytes(4, 'big', signed=True))

        command = [PrivateConstants.STEPPER_MOVE_TO, motor_id]
        for value in position_bytes:
            command.append(value)
        command.append(polarity)

        await self._send_command(command)

    async def stepper_move(self, motor_id, relative_position):
        """
        Set the target position relative to the current position.

        :param motor_id: motor id: 0 - 3

        :param relative_position: The desired position relative to the current
                                  position. Negative is anticlockwise from
                                  the current position. Maximum value is 32 bits.
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_move: Invalid motor_id.')

        polarity = 0

        if relative_position < 0:
            polarity = 1
            relative_position = abs(relative_position)

        position_bytes = list(relative_position.to_bytes(4, 'big', signed=True))

        command = [PrivateConstants.STEPPER_MOVE, motor_id]
        for value in position_bytes:
            command.append(value)
        command.append(polarity)

        await self._send_command(command)

    async def stepper_run(self, motor_id, completion_callback=None):
        """
        This method steps the selected motor based on the current speed.

        Once called, the server will continuously attempt to step the motor.

        :param motor_id: 0 - 3

        :param completion_callback: call back function to receive motion complete
                                    notification

        callback returns a data list:

        [report_type, motor_id, raw_time_stamp]

        The report_type = 19
        """
        if not completion_callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_run: A motion complete callback must be '
                               'specified.')

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_run: Invalid motor_id.')

        self.stepper_info_list[motor_id]['motion_complete_callback'] = completion_callback
        command = [PrivateConstants.STEPPER_RUN, motor_id]
        await self._send_command(command)

    async def stepper_run_speed(self, motor_id):
        """
        This method steps the selected motor based at a constant speed as set by the most
        recent call to stepper_set_max_speed(). The motor will run continuously.

        Once called, the server will continuously attempt to step the motor.

        :param motor_id: 0 - 3

        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_run_speed: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_RUN_SPEED, motor_id]
        await self._send_command(command)

    async def stepper_set_max_speed(self, motor_id, max_speed):
        """
        Sets the maximum permitted speed. The stepper_run() function will accelerate
        up to the speed set by this function.

        Caution: the maximum speed achievable depends on your processor and clock speed.
        The default maxSpeed is 1 step per second.

         Caution: Speeds that exceed the maximum speed supported by the processor may
                  result in non-linear accelerations and decelerations.

        :param motor_id: 0 - 3

        :param max_speed: 1 - 1000
        """

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_max_speed: Invalid motor_id.')

        if not 1 < max_speed <= 1000:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_max_speed: Speed range is 1 - 1000.')

        self.stepper_info_list[motor_id]['max_speed'] = max_speed
        max_speed_msb = (max_speed & 0xff00) >> 8
        max_speed_lsb = max_speed & 0xff

        command = [PrivateConstants.STEPPER_SET_MAX_SPEED, motor_id, max_speed_msb,
                   max_speed_lsb]
        await self._send_command(command)

    async def stepper_get_max_speed(self, motor_id):
        """
        Returns the maximum speed configured for this stepper
        that was previously set by stepper_set_max_speed()

        Value is stored in the client, so no callback is required.

        :param motor_id: 0 - 3

        :return: The currently configured maximum speed.
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_max_speed: Invalid motor_id.')

        return self.stepper_info_list[motor_id]['max_speed']

    async def stepper_set_acceleration(self, motor_id, acceleration):
        """
        Sets the acceleration/deceleration rate.

        :param motor_id: 0 - 3

        :param acceleration: The desired acceleration in steps
                             per second. Must be > 0.0. This is an
                             expensive call since it requires a square
                             root to be calculated on the server.
                             Don't call more often than needed.

        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_acceleration: Invalid motor_id.')

        if not 1 < acceleration <= 1000:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_acceleration: Acceleration range is 1 - '
                               '1000.')

        self.stepper_info_list[motor_id]['acceleration'] = acceleration

        max_accel_msb = acceleration >> 8
        max_accel_lsb = acceleration & 0xff

        command = [PrivateConstants.STEPPER_SET_ACCELERATION, motor_id, max_accel_msb,
                   max_accel_lsb]
        await self._send_command(command)

    async def stepper_set_speed(self, motor_id, speed):
        """
        Sets the desired constant speed for use with stepper_run_speed().

        :param motor_id: 0 - 3

        :param speed: 0 - 1000 The desired constant speed in steps per
                      second. Positive is clockwise. Speeds of more than 1000 steps per
                      second are unreliable. Speed accuracy depends on the ESP32
                      crystal. Jitter depends on how frequently you call the
                      stepper_run_speed() method.
                      The speed will be limited by the current value of
                      stepper_set_max_speed().
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_speed: Invalid motor_id.')

        if not 0 < speed <= 1000:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_speed: Speed range is 0 - '
                               '1000.')

        self.stepper_info_list[motor_id]['speed'] = speed

        speed_msb = speed >> 8
        speed_lsb = speed & 0xff

        command = [PrivateConstants.STEPPER_SET_SPEED, motor_id, speed_msb, speed_lsb]
        await self._send_command(command)

    async def stepper_get_speed(self, motor_id):
        """
        Returns the  most recently set speed.
        that was previously set by stepper_set_speed();

        Value is stored in the client, so no callback is required.

        :param motor_id:  0 - 3

        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_get_speed: Invalid motor_id.')

        return self.stepper_info_list[motor_id]['speed']

    async def stepper_get_distance_to_go(self, motor_id, distance_to_go_callback):
        """
        Request the distance from the current position to the target position
        from the server.

        :param motor_id: 0 - 3

        :param distance_to_go_callback: required callback function to receive report

        :return: The distance to go is returned via the callback as a list:

        [REPORT_TYPE=15, motor_id, distance in steps, time_stamp]

        A positive distance is clockwise from the current position.

        """
        if not distance_to_go_callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'stepper_get_distance_to_go Read: A callback function must be specified.')

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_get_distance_to_go: Invalid motor_id.')
        self.stepper_info_list[motor_id][
            'distance_to_go_callback'] = distance_to_go_callback
        command = [PrivateConstants.STEPPER_GET_DISTANCE_TO_GO, motor_id]
        await self._send_command(command)

    async def stepper_get_target_position(self, motor_id, target_callback):
        """
        Request the most recently set target position from the server.

        :param motor_id: 0 - 3

        :param target_callback: required callback function to receive report

        :return: The distance to go is returned via the callback as a list:

        [REPORT_TYPE=16, motor_id, target position in steps, time_stamp]

        Positive is clockwise from the 0 position.

        """
        if not target_callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'stepper_get_target_position Read: A callback function must be specified.')

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_get_target_position: Invalid motor_id.')

        self.stepper_info_list[motor_id][
            'target_position_callback'] = target_callback

        command = [PrivateConstants.STEPPER_GET_TARGET_POSITION, motor_id]
        await self._send_command(command)

    async def stepper_get_current_position(self, motor_id, current_position_callback):
        """
        Request the current motor position from the server.

        :param motor_id: 0 - 3

        :param current_position_callback: required callback function to receive report

        :return: The current motor position returned via the callback as a list:

        [REPORT_TYPE=17, motor_id, current position in steps, time_stamp]

        Positive is clockwise from the 0 position.
        """
        if not current_position_callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'stepper_get_current_position Read: A callback function must be specified.')

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_get_current_position: Invalid motor_id.')

        self.stepper_info_list[motor_id][
            'current_position_callback'] = current_position_callback

        command = [PrivateConstants.STEPPER_GET_CURRENT_POSITION, motor_id]
        await self._send_command(command)

    async def stepper_set_current_position(self, motor_id, position):
        """
        Resets the current position of the motor, so that wherever the motor
        happens to be right now is considered to be the new 0 position. Useful
        for setting a zero position on a stepper after an initial hardware
        positioning move.

        Has the side effect of setting the current motor speed to 0.

        :param motor_id:  0 - 3

        :param position: Position in steps. This is a 32 bit value
        """

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_current_position: Invalid motor_id.')
        position_bytes = list(position.to_bytes(4, 'big', signed=True))

        command = [PrivateConstants.STEPPER_SET_CURRENT_POSITION, motor_id]
        for value in position_bytes:
            command.append(value)
        await self._send_command(command)

    async def stepper_run_speed_to_position(self, motor_id, completion_callback=None):
        """
        Runs the motor at the currently selected speed until the target position is
        reached.

        Does not implement accelerations.

        :param motor_id: 0 - 3

        :param completion_callback: call back function to receive motion complete
                                    notification

        callback returns a data list:

        [report_type, motor_id, raw_time_stamp]

        The report_type = 19
        """
        if not completion_callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_run_speed_to_position: A motion complete '
                               'callback must be '
                               'specified.')
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_run_speed_to_position: Invalid motor_id.')

        self.stepper_info_list[motor_id]['motion_complete_callback'] = completion_callback
        command = [PrivateConstants.STEPPER_RUN_SPEED_TO_POSITION, motor_id]
        await self._send_command(command)

    async def stepper_stop(self, motor_id):
        """
        Sets a new target position that causes the stepper
        to stop as quickly as possible, using the current speed and
        acceleration parameters.

        :param motor_id:  0 - 3
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_stop: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_STOP, motor_id]
        await self._send_command(command)

    async def stepper_disable_outputs(self, motor_id):
        """
        Disable motor pin outputs by setting them all LOW.

        Depending on the design of your electronics this may turn off
        the power to the motor coils, saving power.

        This is useful to support low power modes: disable the outputs
        during sleep and then re-enable with enableOutputs() before stepping
        again.

        If the enable-Pin is defined, it sets it to OUTPUT mode and clears
        the pin to disabled mode.

        :param motor_id: 0 - 3
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_disable_outputs: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_DISABLE_OUTPUTS, motor_id]
        await self._send_command(command)

    async def stepper_enable_outputs(self, motor_id):
        """
        Enable motor pin outputs by setting the motor pins to OUTPUT
        mode.

        If the enable-Pin is defined, sets it to OUTPUT mode and sets
        the pin to enabled mode.

        :param motor_id: 0 - 3
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_enable_outputs: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_ENABLE_OUTPUTS, motor_id]
        await self._send_command(command)

    async def stepper_set_min_pulse_width(self, motor_id, minimum_width):
        """
        Sets the minimum pulse width allowed by the stepper driver.

        The minimum practical pulse width is approximately 20 microseconds.

        Times less than 20 microseconds will usually result in 20 microseconds or so.

        :param motor_id: 0 -3

        :param minimum_width: A 16 bit unsigned value expressed in microseconds.
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_min_pulse_width: Invalid motor_id.')

        if not 0 < minimum_width <= 0xff:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_min_pulse_width: Pulse width range = '
                               '0-0xffff.')

        width_msb = minimum_width >> 8
        width_lsb = minimum_width & 0xff

        command = [PrivateConstants.STEPPER_SET_MINIMUM_PULSE_WIDTH, motor_id, width_msb,
                   width_lsb]
        await self._send_command(command)

    async def stepper_set_enable_pin(self, motor_id, pin=0xff):
        """
        Sets the enable-pin number for stepper drivers.
        0xFF indicates unused (default).

        Otherwise, if a pin is set, the pin will be turned on when
        enableOutputs() is called and switched off when disableOutputs()
        is called.

        :param motor_id: 0 - 4
        :param pin: 0-0xff
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_enable_pin: Invalid motor_id.')

        if not 0 < pin <= 0xff:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_enable_pin: Pulse width range = '
                               '0-0xff.')
        command = [PrivateConstants.STEPPER_SET_ENABLE_PIN, motor_id, pin]

        await self._send_command(command)

    async def stepper_set_3_pins_inverted(self, motor_id, direction=False, step=False,
                                          enable=False):
        """
        Sets the inversion for stepper driver pins.

        :param motor_id: 0 - 3

        :param direction: True=inverted or False

        :param step: True=inverted or False

        :param enable: True=inverted or False
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_3_pins_inverted: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_SET_3_PINS_INVERTED, motor_id, direction,
                   step, enable]

        await self._send_command(command)

    async def stepper_set_4_pins_inverted(self, motor_id, pin1_invert=False,
                                          pin2_invert=False,
                                          pin3_invert=False, pin4_invert=False,
                                          enable=False):
        """
        Sets the inversion for 2, 3 and 4 wire stepper pins

        :param motor_id: 0 - 3

        :param pin1_invert: True=inverted or False

        :param pin2_invert: True=inverted or False

        :param pin3_invert: True=inverted or False

        :param pin4_invert: True=inverted or False

        :param enable: True=inverted or False
        """
        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_set_4_pins_inverted: Invalid motor_id.')

        command = [PrivateConstants.STEPPER_SET_4_PINS_INVERTED, motor_id, pin1_invert,
                   pin2_invert, pin3_invert, pin4_invert, enable]

        await self._send_command(command)

    async def stepper_is_running(self, motor_id, callback):
        """
        Checks to see if the motor is currently running to a target.

        Callback return True if the speed is not zero or not at the target position.

        :param motor_id: 0-4

        :param callback: required callback function to receive report

        The current running state returned via the callback as a list:

        [REPORT_TYPE=18, motor_id, True or False for running state, time_stamp]
        """
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(
                'stepper_is_running: A callback function must be specified.')

        if not self.stepper_info_list[motor_id]['instance']:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('stepper_is_running: Invalid motor_id.')

        self.stepper_info_list[motor_id]['is_running_callback'] = callback

        command = [PrivateConstants.STEPPER_IS_RUNNING, motor_id]
        await self._send_command(command)

    async def spi_cs_control(self, chip_select_pin, select):
        """
        Control an SPI chip select line

        :param chip_select_pin: pin connected to CS

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

        :param select: 0=select, 1=deselect
        """
        if not self.spi_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'spi_cs_control: SPI interface is not enabled.')

        if chip_select_pin not in self.cs_pins_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'spi_cs_control: chip select pin never enabled.')
        command = [PrivateConstants.SPI_CS_CONTROL, chip_select_pin, select]
        await self._send_command(command)

    async def spi_read_blocking(self, register_selection, number_of_bytes_to_read,
                                call_back=None):
        """
        Read the specified number of bytes from the specified SPI port and
        call the callback function with the reported data.

        :param register_selection: Register to be selected for read.

        :param number_of_bytes_to_read: Number of bytes to read

        :param call_back: Required callback function to report spi data as a
                   result of read command

        callback returns a data list:

        [SPI_READ_REPORT, count of data bytes read, data bytes, time-stamp]

        SPI_READ_REPORT = 13

        """

        if not self.spi_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'spi_read_blocking: SPI interface is not enabled.')

        if not call_back:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('spi_read_blocking: A Callback must be specified')

        self.spi_callback = call_back

        command = [PrivateConstants.SPI_READ_BLOCKING, number_of_bytes_to_read,
                   register_selection]

        await self._send_command(command)

    async def spi_set_format(self, clock_divisor, bit_order, data_mode):
        """
        Configure how the SPI serializes and de-serializes data on the wire.

        See Arduino SPI reference materials for details. The Arduino library is
        used for the ESP32.

        :param clock_divisor:

        :param bit_order:

                            LSBFIRST = 0

                            MSBFIRST = 1 (default)

        :param data_mode:

                            SPI_MODE0 = 0x00 (default)

                            SPI_MODE1  = 0x04

                            SPI_MODE2 = 0x08

                            SPI_MODE3 = 0x0C

        """

        if not self.spi_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'spi_set_format: SPI interface is not enabled.')

        command = [PrivateConstants.SPI_SET_FORMAT, clock_divisor, bit_order,
                   data_mode]
        await self._send_command(command)

    async def spi_write_blocking(self, bytes_to_write):
        """
        Write a list of bytes to the SPI device.

        :param bytes_to_write: A list of bytes to write. This must
                                be in the form of a list.

        """

        if not self.spi_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'spi_write_blocking: SPI interface is not enabled.')

        if type(bytes_to_write) is not list:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('spi_write_blocking: bytes_to_write must be a list.')

        command = [PrivateConstants.SPI_WRITE_BLOCKING, len(bytes_to_write)]

        for data in bytes_to_write:
            command.append(data)

        await self._send_command(command)

    async def set_pin_mode_one_wire(self, pin):
        """
        Initialize the one wire serial bus.

        :param pin: Data pin connected to the OneWire device.

        Valid pins:

           4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33
        """
        self.onewire_enabled = True
        command = [PrivateConstants.ONE_WIRE_INIT, pin]
        await self._send_command(command)

    async def onewire_reset(self, callback=None):
        """
        Reset the onewire device.

        :param callback: required  function to report reset result.

        callback returns:

        [ONEWIRE_REPORT, ONEWIRE_RESET, reset result byte,
                        timestamp]

        Result byte: 1 if a device responds with a presence pulse.  Returns 0 if there
        is no device or the bus is shorted or otherwise held low for more than 250uS

        ONEWIRE_REPORT = 14

        Onewire report subtype ONEWIRE_RESET=29
        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_reset: OneWire interface is not enabled.')
        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_reset: A Callback must be specified')

        self.onewire_callback = callback

        command = [PrivateConstants.ONE_WIRE_RESET]
        await self._send_command(command)

    async def onewire_select(self, device_address):
        """
        Select a device based on its address

        :param device_address: A bytearray of 8 bytes
        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_select: OneWire interface is not enabled.')

        if type(device_address) is not list:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_select: device address must be an array of 8 '
                               'bytes.')

        if len(device_address) != 8:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_select: device address must be an array of 8 '
                               'bytes.')
        command = [PrivateConstants.ONE_WIRE_SELECT]
        for data in device_address:
            command.append(data)
        await self._send_command(command)

    async def onewire_skip(self):
        """
        Skip the device selection. This only works if you have a
        single device, but you can avoid searching and use this to
        immediately access your device.
        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_skip: OneWire interface is not enabled.')

        command = [PrivateConstants.ONE_WIRE_SKIP]
        await self._send_command(command)

    async def onewire_write(self, data, power=0):
        """
        Write a byte to the onewire device. If 'power' is one
        then the wire is held high at the end for
        parasitically powered devices. You
        are responsible for eventually de-powering it by calling
        another read or write.

        :param data: byte to write.

        :param power: power control (see above)
        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_write: OneWire interface is not enabled.')
        if 0 < data < 255:
            command = [PrivateConstants.ONE_WIRE_WRITE, data, power]
            await self._send_command(command)
        else:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_write: Data must be no larger than 255')

    async def onewire_read(self, callback=None):
        """
        Read a byte from the onewire device

        :param callback: required  function to report onewire data as a
                         result of read command


        callback returns a data list:

        [ONEWIRE_REPORT, ONEWIRE_READ, data byte, time-stamp]

        ONEWIRE_REPORT = 14

        Onewire report subtype ONEWIRE_READ=29

        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_read: OneWire interface is not enabled.')

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_read A Callback must be specified')

        self.onewire_callback = callback

        command = [PrivateConstants.ONE_WIRE_READ]
        await self._send_command(command)

    async def onewire_reset_search(self):
        """
        Begin a new search. The next use of search will begin at the first device
        """

        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_reset_search: OneWire interface is not '
                               f'enabled.')
        else:
            command = [PrivateConstants.ONE_WIRE_RESET_SEARCH]
            await self._send_command(command)

    async def onewire_search(self, callback=None):
        """
        Search for the next device. The device address is returned in the callback.
        If a device is found, the 8 byte address is contained in the callback.
        If no more devices are found, the address returned contains all elements set
        to 0xff.

        :param callback: required  function to report a onewire device address

        callback returns a data list:

        [ONEWIRE_REPORT, ONEWIRE_SEARCH=31, 8 byte address, time-stamp]

        ONEWIRE_REPORT = 14

        Onewire report subtype ONEWIRE_SEARCH=31
        """
        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_search: OneWire interface is not enabled.')

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_read A Callback must be specified')

        self.onewire_callback = callback

        command = [PrivateConstants.ONE_WIRE_SEARCH]
        await self._send_command(command)

    async def onewire_crc8(self, address_list, callback=None):
        """
        Compute a CRC check on an array of data.

        :param address_list: a list of bytes

        :param callback: required  function to report a onewire device address

        callback returns a data list:

        [ONEWIRE_REPORT, ONEWIRE_CRC8, CRC, time-stamp]

        ONEWIRE_REPORT = 14

        Onewire report subtype ONEWIRE_CRC8 = 32

        """

        if not self.onewire_enabled:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError(f'onewire_crc8: OneWire interface is not enabled.')

        if not callback:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_crc8 A Callback must be specified')

        if type(address_list) is not list:
            if self.shutdown_on_exception:
                await self.shutdown()
            raise RuntimeError('onewire_crc8: address list must be a list.')

        self.onewire_callback = callback

        address_length = len(address_list)

        command = [PrivateConstants.ONE_WIRE_CRC8, address_length - 1]

        for data in address_list:
            command.append(data)

        await self._send_command(command)

    async def servo_detach(self, pin_number):
        """
        Detach a servo for reuse

        :param pin_number: attached pin
        """
        command = [PrivateConstants.SERVO_DETACH, pin_number]
        await self._send_command(command)

    async def servo_write(self, pin_number, angle):
        """

        Set a servo attached to a pin to a given angle.

        :param pin_number: pin

        :param angle: angle (0-180)

        """
        command = [PrivateConstants.SERVO_WRITE, pin_number, angle]
        await self._send_command(command)

    async def shutdown(self):
        """
        This method attempts an orderly shutdown
        If any exceptions are thrown, they are ignored.

        """
        self.shutdown_flag = True
        # stop all reporting - both analog and digital
        command = [PrivateConstants.STOP_ALL_REPORTS]
        await self._send_command(command)
        if self.restart_on_shutdown:
            # await self.ble_transport.disconnect()
            command = [PrivateConstants.RESET]
            await self._send_command(command)
            await asyncio.sleep(.1)
        if self.the_task:
            self.the_task.cancel()

    async def disable_all_reporting(self):
        """
        Disable reporting for all digital and analog input pins
        """
        command = [PrivateConstants.MODIFY_REPORTING,
                   PrivateConstants.REPORTING_DISABLE_ALL, 0]
        await self._send_command(command)

    async def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.

        :param pin: Analog pin number. For example for A0, the number is 0.

        """
        command = [PrivateConstants.MODIFY_REPORTING,
                   PrivateConstants.REPORTING_ANALOG_DISABLE, pin]
        await self._send_command(command)

    async def disable_digital_reporting(self, pin):
        """
        Disables digital reporting for a single digital pin


        :param pin: GPIO pin number

        """
        command = [PrivateConstants.MODIFY_REPORTING,
                   PrivateConstants.REPORTING_DIGITAL_DISABLE, pin]
        await self._send_command(command)

    async def enable_analog_reporting(self, pin):
        """
        Enables analog reporting for the specified pin.

        :param pin: Analog pin number. For example for A0, the number is 0.


        """
        command = [PrivateConstants.MODIFY_REPORTING,
                   PrivateConstants.REPORTING_ANALOG_ENABLE, pin]
        await self._send_command(command)

    async def enable_digital_reporting(self, pin):
        """
        Enable reporting on the specified digital pin.

        :param pin: GPIO Pin number.
        """

        command = [PrivateConstants.MODIFY_REPORTING,
                   PrivateConstants.REPORTING_DIGITAL_ENABLE, pin]
        await self._send_command(command)

    async def _ble_report_dispatcher(self, sender=None, data=None):
        """
        This is a private method called by the incoming data notifier

        Using the report identifier, the report handler is fetched from report_dispatch.

        :param sender: BLE sender ID
        :param data: data received over the ble link

        """
        self.the_sender = sender
        report = data[1]

        # noinspection PyArgumentList
        await self.report_dispatch[report](data[2:])

    # noinspection PyArgumentList
    async def _wifi_report_dispatcher(self):
        """
        This is a private method.
        It continually accepts and interprets data coming from Telemetrix4Arduino,and then
        dispatches the correct handler to process the data.

        It first receives the length of the packet, and then reads in the rest of the
        packet. A packet consists of a length, report identifier and then the report data.
        Using the report identifier, the report handler is fetched from report_dispatch.

        :returns: This method never returns
        """

        while True:
            if self.shutdown_flag:
                break
            try:
                packet_length = ord(await self.transport.read())
            except TypeError:
                continue

            # get the rest of the packet
            packet = list(await self.transport.read(packet_length))

            report = packet[0]
            # print(report)
            # handle all other messages by looking them up in the
            # command dictionary

            # await self.report_dispatch[report](packet[1:])
            await self.report_dispatch[report](packet[1:])

    '''
    Report message handlers
    '''

    async def _report_loop_data(self, data):
        """
        Print data that was looped back

        :param data: byte of loop back data
        """
        if self.loop_back_callback:
            await self.loop_back_callback(data)

    # noinspection PyMethodMayBeStatic
    async def _report_debug_data(self, data):
        """
        Print debug data sent from the ESP32 server.

        :param data: data[0] is a byte followed by 2
                     bytes that comprise an integer
        """
        value = (data[1] << 8) + data[2]
        print(f'DEBUG ID: {data[0]} Value: {value}')

    async def _analog_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for analog messages.

        :param data: message data

        """
        data = list(data)
        pin = data[0]
        value = (data[1] << 8) + data[2]

        time_stamp = time.time()

        # append pin number, pin value, and pin type to return value and return as a list
        message = [PrivateConstants.AT_ANALOG, pin, value, time_stamp]

        await self.analog_callbacks[pin](message)

    async def _dht_report(self, data):
        """
        This is a private message handler for dht addition errors

        :param data:    data[0] = report subtype - DHT_DATA or DHT_ERROR

                        data[1] = pin number

                        data[2] = humidity high order byte or error value if DHT_ERROR

                        data[3] = humidity byte 2

                        data[4] = humidity byte 3

                        data[5] = humidity byte 4

                        data[6] = temperature high order byte for data

                        data[7] = temperature byte 2

                        data[8] = temperature byte 3

                        data[9] = temperature byte 4
        """

        if data[0]:
            # error report
            # data[0] = report sub type, data[1] = pin, data[2] = error message
            if self.dht_callbacks[data[1]]:
                message = [PrivateConstants.DHT_REPORT, data[0], data[1], data[2],
                           time.time()]
                await self.dht_callbacks[data[1]](message)
        else:
            # got valid data
            f_humidity = bytearray(data[2:6])
            f_temperature = bytearray(data[6:])
            message = [PrivateConstants.DHT_REPORT, data[0], data[1],
                       (struct.unpack('<f', f_humidity))[0],
                       (struct.unpack('<f', f_temperature))[0],
                       time.time()]
            await self.dht_callbacks[data[1]](message)

    async def _digital_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for Digital Messages.

        :param data: digital message

        """
        pin = data[0]
        value = data[1]

        time_stamp = time.time()
        if self.digital_callbacks[pin]:
            message = [PrivateConstants.DIGITAL_REPORT, pin, value, time_stamp]
            await self.digital_callbacks[pin](message)

    async def _servo_unavailable(self, report):
        """
        Message if no servos are available for use.

        :param report: GPIO pin number
        """
        if self.shutdown_on_exception:
            await self.shutdown()
        raise RuntimeError(
            f'Servo Attach For Pin {report[0]} Failed: No Available Servos')

    async def _i2c_read_report(self, data):
        """
        Execute callback for i2c reads.

        :param data: [I2C_READ_REPORT, number of bytes read, address, register,
                      bytes read..., time-stamp]
        """

        # we receive [# data bytes, address, register, data bytes]
        # number of bytes of data returned

        # data[0] = number of bytes
        # data[1] = number of bytes returned
        # data[2] = address
        # data[3] = register
        # data[4] ... all the data bytes

        data = list(data)

        cb_list = [PrivateConstants.I2C_READ_REPORT, data[0], data[1]] + data[2:]
        cb_list.append(time.time())

        await self.i2c_callback(cb_list)

    async def _i2c_too_few(self, data):
        """
        I2c reports too few bytes received

        :param data: data[0] = device address
        """
        if self.shutdown_on_exception:
            await self.shutdown()
        raise RuntimeError(
            f'i2c too few bytes received from i2c port {data[0]} i2c address {data[1]}')

    async def _i2c_too_many(self, data):
        """
        I2c reports too few bytes received

        :param data: data[0] = device address
        """
        if self.shutdown_on_exception:
            await self.shutdown()
        raise RuntimeError(
            f'i2c too many bytes received from i2c port {data[0]} i2c address {data[1]}')

    async def _sonar_distance_report(self, report):
        """

        :param report: data[0] = trigger pin, data[1] and data[2] = distance

        callback report format: [PrivateConstants.SONAR_DISTANCE, trigger_pin, distance_value, time_stamp]
        """

        # get callback from pin number
        cb = self.sonar_callbacks[report[0]]

        # build report data
        cb_list = [PrivateConstants.SONAR_DISTANCE, report[0],
                   ((report[1] << 8) + report[2]), time.time()]

        await cb(cb_list)

    async def _touch_report(self, report):
        """
        This is a private message handler method.
        It is a message handler for touch pin messages.

        :param report: message data

        """
        pin = report[0]
        value = (report[1] << 8) + report[2]
        # set the current value in the pin structure
        time_stamp = time.time()
        if self.touch_callbacks[pin]:
            message = [PrivateConstants.TOUCH_REPORT, pin, value, time_stamp]
            await self.touch_callbacks[pin](message)

    async def _spi_report(self, report):

        report = list(report)

        cb_list = [PrivateConstants.SPI_REPORT, report[0]] + report[1:]

        cb_list.append(time.time())

        await self.spi_callback(cb_list)

    async def _onewire_report(self, report):
        report = list(report)
        cb_list = [PrivateConstants.ONE_WIRE_REPORT, report[0]] + report[1:]
        cb_list.append(time.time())
        await self.onewire_callback(cb_list)

    async def _firmware_report(self, report):
        self.firmware_version = report

    async def _stepper_distance_to_go_report(self, report):
        """
        Report stepper distance to go.

        :param report: data[0] = motor_id, data[1] = steps MSB, data[2] = steps byte 1,
                                 data[3] = steps bytes 2, data[4] = steps LSB

        callback report format: [PrivateConstants.STEPPER_DISTANCE_TO_GO, motor_id
                                 steps, time_stamp]
        """

        # get callback
        cb = self.stepper_info_list[report[0]]['distance_to_go_callback']

        # isolate the steps bytes and covert list to bytes
        steps = bytes(report[1:])

        # get value from steps
        num_steps = int.from_bytes(steps, byteorder='big', signed=True)

        cb_list = [PrivateConstants.STEPPER_DISTANCE_TO_GO, report[0], num_steps,
                   time.time()]

        await cb(cb_list)

    async def _stepper_target_position_report(self, report):
        """
        Report stepper target position to go.

        :param report: data[0] = motor_id, data[1] = target position MSB,
                       data[2] = target position byte MSB+1
                       data[3] = target position byte MSB+2
                       data[4] = target position LSB

        callback report format: [PrivateConstants.STEPPER_TARGET_POSITION, motor_id
                                 target_position, time_stamp]
        """

        # get callback
        cb = self.stepper_info_list[report[0]]['target_position_callback']

        # isolate the steps bytes and covert list to bytes
        target = bytes(report[1:])

        # get value from steps
        target_position = int.from_bytes(target, byteorder='big', signed=True)

        cb_list = [PrivateConstants.STEPPER_TARGET_POSITION, report[0], target_position,
                   time.time()]

        await cb(cb_list)

    async def _stepper_current_position_report(self, report):
        """
        Report stepper current position.

        :param report: data[0] = motor_id, data[1] = current position MSB,
                       data[2] = current position byte MSB+1
                       data[3] = current position byte MSB+2
                       data[4] = current position LSB

        callback report format: [PrivateConstants.STEPPER_CURRENT_POSITION, motor_id
                                 current_position, time_stamp]
        """

        # get callback
        cb = self.stepper_info_list[report[0]]['current_position_callback']

        # isolate the steps bytes and covert list to bytes
        position = bytes(report[1:])

        # get value from steps
        current_position = int.from_bytes(position, byteorder='big', signed=True)

        cb_list = [PrivateConstants.STEPPER_CURRENT_POSITION, report[0], current_position,
                   time.time()]

        await cb(cb_list)

    async def _stepper_is_running_report(self, report):
        """
        Report if the motor is currently running

        :param report: data[0] = motor_id, True if motor is running or False if it is not.

        callback report format: [18, motor_id,
                                 running_state, time_stamp]
        """

        # get callback
        cb = self.stepper_info_list[report[0]]['is_running_callback']

        cb_list = [PrivateConstants.STEPPER_RUNNING_REPORT, report[0], time.time()]

        await cb(cb_list)

    async def _stepper_run_complete_report(self, report):
        """
        The motor completed it motion

        :param report: data[0] = motor_id

        callback report format: [PrivateConstants.STEPPER_RUN_COMPLETE_REPORT, motor_id,
                                 time_stamp]
        """

        # get callback
        cb = self.stepper_info_list[report[0]]['motion_complete_callback']

        cb_list = [PrivateConstants.STEPPER_RUN_COMPLETE_REPORT, report[0],
                   time.time()]

        await cb(cb_list)

    async def _send_command(self, command):
        """
        This is a private utility method.


        :param command:  command data in the form of a list

        :returns: number of bytes sent
        """
        # the length of the list is added at the head
        command.insert(0, len(command))
        # print(command)
        send_message = bytes(command)
        await self.transport.write(send_message)