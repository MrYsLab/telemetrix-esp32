When you set a pin mode to one of the several input pin mode types, you must 
specify a callback function. When the state or value of the input changes, the
callback function is called to handle the change.

Callbacks provide immediate feedback when a data change occurs. 

For example, we use the following API call to set 
pin 4 as a digital input pin with pullups enabled.

```python
board.set_pin_mode_digital_input_pullup(4, the_callback)

```
Here is an example of a callback function that prints the change to the console.
```python
def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin mode, pin, current reported value, pin_mode, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Report Type: {data[CB_PIN_MODE]} Pin: {data[CB_PIN]} '
          f'Value: {data[CB_VALUE]} Time Stamp: {date}')

```
The **data** parameter passed to the callback function is in the form of a list. It 
always contains the origin of the callback, such as a digital or 
analog input, and a timestamp for the data change occurrence.

The contents of the data parameter are specified in the API for each set_pin_mode method.
For example:

```python

  def set_pin_mode_digital_input_pullup(self, pin_number, callback)

    Set a pin as a digital input with pullup enabled.

    :param pin_number: GPIO pin number

    Valid pins:

     4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

    :param callback: callback function

    callback returns a data list:

    [report_type, pin_number, pin_value, raw_time_stamp]

    The report_type for digital input pins with pullups enabled = 2
```

This list contains: **[pin_type, pin_number, pin_value, raw_time_stamp]**
The pin type for this pin mode is 2.
<br>
<br>


Copyright (C) 2022 Alan Yorinks. All Rights Reserved.