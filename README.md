# Telemetrix For The ESP32

# UNDER CONSTRUCTION

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

This project consists of three python clients, two for WI-FI and one for BLE. 

With WI-FI, you may choose between two APIs. For a "standard" Python
threaded environment, then choose this [telemetrix-esp32 API]().
If you prefer to work in an asyncio environment, then choose the [telemetrix-aio-esp32 
API]().

The [BLE API]() only supports asyncio only. This is due to the limitations of the 
available Python BLE libraries.

A [User's Guide](https://mryslab.github.io/telemetrix/) explaining installation and use is available online.



