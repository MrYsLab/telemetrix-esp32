## Pin Modes
Before utilizing a pin, you must set its pin mode. Check the APIs for methods that 
begin with _set_pin_mode_ in their name for the available modes.


## Specifying Pin Numbers

### Valid Pin Numbers
A subset of the GPIO PINS is available when setting pin modes.
The valid pins available for a specific pin mode are shown in the API. For example:

```angular2html
 def set_pin_mode_digital_input(self, pin_number, callback)

    Set a pin as a digital input.

    :param pin_number: GPIO pin number.

    Valid pins:

    4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

    :param callback: callback function

    callback returns a data list:

    [report_type, pin_number, pin_value, raw_time_stamp]

    The report_type for digital input pins = 2
```

The set of valid pins are based on the work of [Andreas Spiess](https://www.youtube.com/watch?v=LY-1DHTxRAk)

GPIO pin numbers are used for all pin modes.

### SPI Pins
Telemetrix uses the standard SPI pins. Only the chip select pins (cs) need to be 
specified.

    CS =    5
    MOSI =  23
    MISO =  19
    SCK =   18


### I2C Pins
Telemetrix uses the standard I2C pins.
    (SDA) - 21
    (SCL) - 22


<br>
<br>
Copyright (C) 2022 Alan Yorinks. All Rights Reserved.
