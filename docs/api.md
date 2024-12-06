When developing an application, refer to the client API documentation for the available 
methods and their input parameters. 


## Online API Documentation For The WI-FI And BLE Threaded Client

**NOTE: Windows on the threaded BLE API is not supported**

* The [WI-FI and BLE threaded client](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_esp32/index.html) 

When working with the threaded client, to work with BLE, set the 
**_transport_is_wifi_** parameter to False. The MAC address is automatically 
discovered, but if you wish to specify the MAC address explicitly, you may do so by 
setting the **_transport address_** parameter.

For WI-FI, you must specify the IP Address assigned
to the ESP32 device. This is accomplished with the **_transport_address parameter_**.

```angular2html
 class TelemetrixEsp32 (transport_address=None, ip_port=31336, autostart=True, 
                        shutdown_on_exception=True, restart_on_shutdown=True) 
```

## Online API Documentation For The Asyncio Client For Both WI-FI And BLE

* The [WI-FI and BLE asyncio client](https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-esp32/blob/master/html/telemetrix_aio_esp32/index.html)

When working with the asyncio client, to work with BLE, set the 
**_transport_is_wifi_** parameter to False. The MAC address is automatically 
discovered, but if you wish to specify the MAC address explicitly, you may do so by 
setting the **_transport address_** parameter.

When working with the WI-FI client, you must specify the IP Address assigned to the 
ESP32 device. This is accomplished with the **_transport_address parameter_**.

```angular2html
 class TelemetrixAioEsp32 (transport_is_wifi=True, transport_address=None, ip_port=31336,
       autostart=True, loop=None, shutdown_on_exception=True, restart_on_shutdown=True) 
```

## Examples
An extensive set of examples is provided as part of the release. Refer to the links
in the [**_Examples_** table on this page.](../#examples) 


