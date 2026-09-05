# IOT_LAB-2-assignment

# LAB1: Temperature Sensor with Relay Control Using Telegram

## 1. Overview

This project is an IoT temperature monitoring and relay control system using an ESP32, temperature/humidity sensor, relay module, Wi-Fi, and Telegram Bot API.

The ESP32 reads the temperature and humidity every 5 seconds.

The Telegram bot allows the user to:
- Use `/status` to check temperature, humidity, and relay state.
- Use `/on` to turn the relay ON.
- Use `/off` to turn the relay OFF.

When the temperature is 25°C or higher and the relay is OFF, the ESP32 sends a warning message every 5 seconds.

When the user sends `/on`, the relay turns ON and the warning messages stop.

When the temperature drops below 25°C, the relay automatically turns OFF and sends a one-time auto-OFF message.


## 2. Equipment

The equipment used in this lab:

- ESP32 Development Board
- DHT temperature and humidity sensor
- 1-channel relay module
- Jumper wires
- USB cable
- Laptop with Thonny
- Wi-Fi connection
- Telegram application


## 3. Wiring

The components are connected to the ESP32 as follows:

| Component | ESP32 Pin |
|-----------|-----------|
| DHT VCC | 3.3V |
| DHT GND | GND |
| DHT DATA | GPIO 4 |
| Relay VCC | 5V |
| Relay GND | GND |
| Relay IN | GPIO [YOUR RELAY GPIO] |

### Wiring Photo

![Wiring](Component.jpg)


## 4. Software Setup

The ESP32 uses MicroPython and the program was written using Thonny IDE.

The main libraries used are:

```python
from machine import Pin
import dht
import network
import time
import urequests
```
###5. Flowchart

![Alternative Text](folder-name/your-photo-name.jpg)

![Flowchart](Flowchart.drawio.png)
