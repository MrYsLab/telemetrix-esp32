# Debugging Aids

## loopback
This loop_back API method allows you to verify that communication between the client 
and server is functional.

```python
 def loop_back(self, start_character, callback=None)

    This is a debugging method to send a character to the Arduino device, and have the device loop it back.

    :param start_character: The character to loop back. It should be an integer.

    :param callback: Looped back character will appear in the callback method
```


<br>
<br>
Copyright (C) 2021 Alan Yorinks. All Rights Reserved.
