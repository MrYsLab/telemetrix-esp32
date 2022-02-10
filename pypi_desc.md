# Telemetrix For The ESP32

Would you like to remotely control and monitor an ESP32 device from your PC using either 
a  WI-FI or Bluetooth Low Energy (BLE) transport? This package provides everything you 
need to 
do so.

It consists of Python client APIs to construct your application and firmware 
installed on the ESP32 device.

The firmware uploaded to the ESP32 device 
takes advantage of the [Arduino Core For The ESP32.](https://github.com/espressif/arduino-esp32)
As a result, the [Arduino IDE](https://www.arduino.cc/en/software)
is used to compile and upload the firmware to the device.

It is compatible with Windows, Linux, and macOS. It requires the use of Python 3.7 or 
greater.

The following features are supported:

* Analog Input           
* Analog Output (PWM)  
* Analog Output (DAC)  
* Digital Input          
* Digital Output         
* ESP32 Touch Pin Input  
* i2c Primitives   
* OneWire Primitives   
* SPI Primitives     
* DHT Temperature/Humidity Sensor Support  
* HC-SR04 Sonar Distance Sensor Support   
* Servo Motor Control   
* Stepper Motor Control (AccelStepper) 
* Both WI-FI and BLE Transports Supported
* Available Online Client APIs:
  * [WI-FI Threaded Model](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_esp32/index.html)
  * [WI-FI And BLE Asyncio Model](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_aio_esp32/index.html)
* Callbacks provide immediate notifications for fast and efficient input 
data change notifications.
* The Code Is Designed To Be User Extensible
* Integrated Client/Server Debugging Aids Are Included


A complete set of examples is included. 
Use the horizontal scroll bar at the bottom of the features table to view all the links.

| Feature                           | Feature Type              | WI-FI ExampleS                                                                                                                               | WI-FI Asyncio Examples                                                                                                                                   | BLE Asyncio Examples                                                                                                                                  |
|-----------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Analog Input                      | GPIO                      | [analog_input_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/analog_input_wifi.py)                           | [analog_input_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/analog_input_wifi_aio.py)                           | [analog_input_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/analog_input_ble_aio.py)                           |
| Analog Output (PWM)               | GPIO                      | [fade_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/fade_wifi.py)                                           | [fade_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/fade_wifi_aio.py)                                           | [fade_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/fade_ble_aio.py)                                           |
| Analog Output (DAC)               | GPIO                      | [dac_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/dac_wifi.py)                                             | [dac_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/dac_wifi_aio.py)                                             | [dac_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/dac_ble.py)                                                 |
| Digital Input                     | GPIO                      | [digital_input_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_wifi.py)                         | [digital_input_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_wifi_aio.py)                         | [digital_input_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_ble.py)                             |
| Digital Input Pull Down           | GPIO                      | [digital_input_pulldown_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_pulldown_wifi.py)       | [digital_input_pulldown_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_pulldown_wifi_aio.py)       | [digital_input_pulldown_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_pulldown_ble.py)           |
| Digital Input Pull Up             | GPIO                      | [digital_input_pullup_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_pullup_wifi.py)           | [digital_input_pullup_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_pullup_wifi_aio.py)           | [digital_input_pullup_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_pullup_ble.py)               |
| Digital Output                    | GPIO                      | [blink_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/blink_wifi.py)                                         | [blink_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/blink_wifi_aio.py)                                         | [blink_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/blink_ble_aio.py)                                         |
| Touch Pin Input                   | GPIO                      | [touch_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/touch_input_wifi.py)                                   | [touch_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/touch_input_wifi_aio.py)                                   | [touch_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/touch_input_ble_aio.py)                                   |
| i2c (ADXL345 Accelerometer)       | Device Communications Bus | [i2c_adxl345_accelerometer_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/i2c_adxl345_accelerometer_wifi.py) | [i2c_adxl345_accelerometer_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/i2c_adxl345_accelerometer_wifi_aio.py) | [i2c_adxl345_accelerometer_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/i2c_adxl345_accelerometer_ble_aio.py) |
| OneWire (DS18x20 Thermometer)     | Device Communications Bus | [onewire_ds18x20_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/onewire_ds18x20_wifi.py)                     | [onewire_ds18x20_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/onewire_ds18x20_wifi_aio.py)                     | [onewire_ds18x20_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/onewire_ds18x20_ble_aio.py)                     |
| SPI (MPU9250 Accelerometer)       | Device Communications Bus | [spi_mpu9250_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/spi_mpu9250_wifi.py)                             | [spi_mpu9250_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/spi_mpu9250_wifi_aio.py)                             | [spi_mpu9250_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/spi_mpu9250_ble_aio.py)                             |
| DHT Temperature/Humidity Sensor   | Sensor Device Support     | [dht_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/dht_wifi.py)                                             | [dht_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/dht_wifi_aio.py)                                             | [dht_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/dht_ble_aio.py)                                             |
| HC-SR04 Sonar Distance Sensor     | Sensor Device Support     | [hc-sr04_distance_sensor_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/hc-sr04_distance_sensor_wifi.py)     | [hc-sr04_distance_sensor_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/hc-sr04_distance_sensor_wifi_aio.py)     | [hc-sr04_distance_sensor_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/hc-sr04_distance_sensor_ble_aio.py)     |
| Servo Motor                       | Motor Control             | [servo_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/servo_wifi.py)                                         | [servo_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/servo_wifi_aio.py)                                         | [servo_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/servo_ble_aio.py)                                         |
| Stepper Motor (Absolute Position) | Motor Control             | [stepper_absolute_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_absolute_wifi.py)                   | [stepper_absolute_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_absolute_wifi_aio.py)                   | [stepper_absolute_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_absolute_ble_aio.py)                   |
| Stepper Motor (Continuous Motion) | Motor Control             | [stepper_continuous_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_continuous_wifi.py)               | [stepper_continuous_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_continuous_wifi_aio.py)               | [stepper_continuous_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_continuous_ble_aio.py)               |
| Stepper Motor (Relative Position) | Motor Control             | [stepper_relative_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_relative_wifi.py)                   | [stepper_relative_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_relative_wifi_aio.py)                   | [stepper_relative_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_relative_ble_aio.py)                   |
| Transport Loopback Diagnostic     | System Diagnostic         | [loop_back_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/loop_back_wifi.py)                                 | [loop_back_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/loop_back_wifi_aio.py)                                 | [loop_back_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/loop_back_ble_aio.py)                                 |

A [User's Guide]() explaining installation and use is available online.




Would you like to remotely control and monitor an ESP32 device from your PC using either 
a  WI-FI or Bluetooth Low Energy (BLE) transport? This package provides everything you 
need to 
do so.

It consists of Python client APIs used to construct your application, and the firmware 
for the ESP32 device is built using [Arduino Core For The ESP32.](https://github.com/espressif/arduino-esp32)

Using an Arduino core as the basis for the firmware allows you to use the Arduino IDE to
compile and upload the firmware to the ESP32.

Callbacks provide immediate notifications for fast and efficient input 
data change notifications.

It is compatible with Windows, Linux, and macOS. It requires the use of Python 3.7 or 
greater.

The following features are supported:

* Analog Input           
* Analog Output (PWM)  
* Analog Output (DAC)  
* Digital Input          
* Digital Output         
* ESP32 Touch Pin Input  
* i2c Primitives   
* OneWire Primitives   
* SPI Primitives     
* DHT Temperature/Humidity Sensor Support  
* HC-SR04 Sonar Distance Sensor Support   
* Servo Motor Control   
* Stepper Motor Control (AccelStepper) 
* Both WI-FI and BLE Transports Supported
* Available Online Client APIs:
  * [WI-FI Threaded Model](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_esp32/index.html)
  * [WI-FI And BLE Asyncio Model](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_aio_esp32/index.html)
* The Code Is Designed To Be User Extensible
* Integrated Client/Server Debugging Aids Are Included


A complete set of examples is included. 
Use the horizontal scroll bar at the bottom of the features table to view all the links.

| Feature                           | Feature Type              | WI-FI ExampleS                                                                                                                               | WI-FI Asyncio Examples                                                                                                                                   | BLE Asyncio Examples                                                                                                                                  |
|-----------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Analog Input                      | GPIO                      | [analog_input_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/analog_input_wifi.py)                           | [analog_input_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/analog_input_wifi_aio.py)                           | [analog_input_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/analog_input_ble_aio.py)                           |
| Analog Output (PWM)               | GPIO                      | [fade_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/fade_wifi.py)                                           | [fade_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/fade_wifi_aio.py)                                           | [fade_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/fade_ble_aio.py)                                           |
| Analog Output (DAC)               | GPIO                      | [dac_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/dac_wifi.py)                                             | [dac_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/dac_wifi_aio.py)                                             | [dac_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/dac_ble.py)                                                 |
| Digital Input                     | GPIO                      | [digital_input_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_wifi.py)                         | [digital_input_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_wifi_aio.py)                         | [digital_input_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_ble.py)                             |
| Digital Input Pull Down           | GPIO                      | [digital_input_pulldown_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_pulldown_wifi.py)       | [digital_input_pulldown_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_pulldown_wifi_aio.py)       | [digital_input_pulldown_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_pulldown_ble.py)           |
| Digital Input Pull Up             | GPIO                      | [digital_input_pullup_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/digital_input_pullup_wifi.py)           | [digital_input_pullup_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/digital_input_pullup_wifi_aio.py)           | [digital_input_pullup_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/digital_input_pullup_ble.py)               |
| Digital Output                    | GPIO                      | [blink_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/blink_wifi.py)                                         | [blink_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/blink_wifi_aio.py)                                         | [blink_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/blink_ble_aio.py)                                         |
| Touch Pin Input                   | GPIO                      | [touch_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/touch_input_wifi.py)                                   | [touch_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/touch_input_wifi_aio.py)                                   | [touch_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/touch_input_ble_aio.py)                                   |
| i2c (ADXL345 Accelerometer)       | Device Communications Bus | [i2c_adxl345_accelerometer_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/i2c_adxl345_accelerometer_wifi.py) | [i2c_adxl345_accelerometer_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/i2c_adxl345_accelerometer_wifi_aio.py) | [i2c_adxl345_accelerometer_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/i2c_adxl345_accelerometer_ble_aio.py) |
| OneWire (DS18x20 Thermometer)     | Device Communications Bus | [onewire_ds18x20_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/onewire_ds18x20_wifi.py)                     | [onewire_ds18x20_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/onewire_ds18x20_wifi_aio.py)                     | [onewire_ds18x20_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/onewire_ds18x20_ble_aio.py)                     |
| SPI (MPU9250 Accelerometer)       | Device Communications Bus | [spi_mpu9250_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/spi_mpu9250_wifi.py)                             | [spi_mpu9250_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/spi_mpu9250_wifi_aio.py)                             | [spi_mpu9250_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/spi_mpu9250_ble_aio.py)                             |
| DHT Temperature/Humidity Sensor   | Sensor Device Support     | [dht_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/dht_wifi.py)                                             | [dht_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/dht_wifi_aio.py)                                             | [dht_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/dht_ble_aio.py)                                             |
| HC-SR04 Sonar Distance Sensor     | Sensor Device Support     | [hc-sr04_distance_sensor_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/hc-sr04_distance_sensor_wifi.py)     | [hc-sr04_distance_sensor_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/hc-sr04_distance_sensor_wifi_aio.py)     | [hc-sr04_distance_sensor_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/hc-sr04_distance_sensor_ble_aio.py)     |
| Servo Motor                       | Motor Control             | [servo_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/servo_wifi.py)                                         | [servo_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/servo_wifi_aio.py)                                         | [servo_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/servo_ble_aio.py)                                         |
| Stepper Motor (Absolute Position) | Motor Control             | [stepper_absolute_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_absolute_wifi.py)                   | [stepper_absolute_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_absolute_wifi_aio.py)                   | [stepper_absolute_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_absolute_ble_aio.py)                   |
| Stepper Motor (Continuous Motion) | Motor Control             | [stepper_continuous_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_continuous_wifi.py)               | [stepper_continuous_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_continuous_wifi_aio.py)               | [stepper_continuous_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_continuous_ble_aio.py)               |
| Stepper Motor (Relative Position) | Motor Control             | [stepper_relative_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/stepper_relative_wifi.py)                   | [stepper_relative_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/stepper_relative_wifi_aio.py)                   | [stepper_relative_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/stepper_relative_ble_aio.py)                   |
| Transport Loopback Diagnostic     | System Diagnostic         | [loop_back_wifi.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi/loop_back_wifi.py)                                 | [loop_back_wifi_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/wifi-aio/loop_back_wifi_aio.py)                                 | [loop_back_ble_aio.py](https://github.com/MrYsLab/telemetrix-esp32/blob/master/examples/ble-aio/loop_back_ble_aio.py)                                 |

A [User's Guide]() explaining installation and use is available online.