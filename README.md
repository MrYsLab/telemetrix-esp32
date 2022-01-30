# Telemetrix For The ESP32

The Telemetrix Project is a modern-day replacement for 
StandardFirmata and comes equipped with many more built-in features than 
StandardFirmata. 

Here is a feature comparison between Telemetrix and StandardFirmata:

| Feature | Telemetrix | StandardFirmata |
|-------|:----------:|:-----------------:|
|     Analog Input    |       X     |      X           |
|     Analog Output (PWM)    |       X     |      X           |
|     Digital Input    |       X     |      X           |
|     Digital Output    |       X     |      X           |
|     i2c Primitives  |       X     |      X           |
|     Servo Motor Control  |       X     |      X           |
|     DHT Temperature/Humidity Sensor  |       X     |                 |
|     OneWire Primitives |       X     |                 |
|     HC-SR04 Sonar Distance Sensor  |       X     |                 |
|     SPI Primitives  |       X     |                 |
|     Stepper Motor Control (AccelStepper) |       X     |                 |
|    Python Threaded Client Included  |       X     |      
|    Python Asyncio Client Included  |       X     |
|    Designed To Be User Extensible |       X     |                 |
|    Integrated Debugging Aids Provided |       X     |                 |
|    Examples For All Features |       X     |                 |

With WI-FI, you have a choice of two different APIs. The telemetrix_esp32 API uses 
Python threading, while telemetrix_aio_esp32 uses Python asyncio.

The BLE API only supports an asyncio version. This is due to the limitations of the 
available Python BLE libraries.

Here are links to the various client APIs:

[WI-FI Threaded](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html)
[WI-FI Asyncio](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html)

[BLE Asyncio](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html)

The project consists of a 
[Python client API](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html)
used to create a Python 
client 
application and C++ servers that communicate with the Python client over a serial or WiFi link. 

This repository is the Python 3 asyncio client API.

The server for Arduino serial linked devices is called
[Telemetrix4Arduino](https://github.com/MrYsLab/Telemetrix4Arduino).

The WiFi server for ESP8266 devices is called
[Telemetrix4Esp8266](https://github.com/MrYsLab/Telemetrix4Esp8266).

A [User's Guide](https://mryslab.github.io/telemetrix/) explaining installation and use is available online.



