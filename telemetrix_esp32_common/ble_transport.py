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

from bleak import discover
from bleak import BleakClient
import asyncio
import sys


# noinspection PyStatementEffect,PyUnresolvedReferences,PyUnresolvedReferences
class BleTransport:
    """
    This class encapsulates management of the BLE transport
    """

    def __init__(self, ble_mac_address=None,
                 loop=None, receive_callback=None, is_asyncio=True):
        """

        :param ble_mac_address: User specified mac address. If not specified
                                mac address discovery will be attempted.

        :param loop: asyncio loop

        :param receive_callback: method to be called when data is received

        :param is_asyncio: set to True for an asyncio app or False for
                           non-asyncio

        """

        if not receive_callback:
            raise RuntimeError('ble_aio_transport: A receive callback must be specified')

        if not is_asyncio:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.ble_mac_address = ble_mac_address

        self.receive_callback = receive_callback

        self.UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # Nordic NUS characteristic for TX
        self.UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # Nordic NUS characteristic for RX

        self.client = None

        self.the_task = None

        self.connected = False

        self.is_asyncio = is_asyncio

    async def notification_handler(self, sender, data):
        """
        Process incoming BLE data
        Call the incoming data processing method
        :param sender: sender ID - not used
        :param data: data received
        """

        if self.is_asyncio:
            await self.receive_callback(sender, data)
        else:
            self.receive_callback(sender, data)

    def ble_connect(self):
        try:
            self.loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            raise

    # noinspection PyTypeChecker
    async def connect(self):
        """
        This method will attempt a connection with the ble device if not already connected.

        If a ble MAC address was provided it will use that address, and if not,
        it will attempt to auto discover the device before connection

        """
        if self.connected:
            raise RuntimeError('ble_aio_transport: connect - Already connected')

        if not self.ble_mac_address:
            print('Retrieving BLE Mac Address of Ble Device. Please wait...')
            devices = await discover()
            for d in devices:
                if d.name == 'Telemetrix4ESP32BLE':
                    self.ble_mac_address = d.address

        # now attempt to connect
        print(f'Connecting to {self.ble_mac_address}. Please wait....')
        self.client = BleakClient(self.ble_mac_address)
        await self.client.connect()
        self.connected = True
        print('Connection successful')

        # associate the notification handler with incoming data
        await self.client.start_notify(self.UART_RX_UUID, self.notification_handler)

    async def disconnect(self):
        await self.client.disconnect()

    def ble_write(self, data):
        self.loop.run_until_complete(self.write(data))

    async def write(self, data):

        """
        This method writes sends data to the BLE device
        :param data: data is in the form of a bytearray

        """
        # noinspection PyBroadException
        try:
            await self.client.write_gatt_char(self.UART_TX_UUID, data)
        except Exception:
            pass

        if sys.platform.startswith('win32'):
            await asyncio.sleep(.2)
