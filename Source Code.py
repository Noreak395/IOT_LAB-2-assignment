import network
import urequests
import time
from machine import Pin
import dht

# ---------- WIFI ----------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

# ---------- TELEGRAM ----------
BOT_TOKEN = "8772539654:AAEhnpAZmFFhjpJZyO_re5tb6r9oMDLxRlY"
CHAT_ID = "-5463703065"

URL_SEND = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)
URL_GET = "https://api.telegram.org/bot{}/getUpdates".format(BOT_TOKEN)

last_id = 0


# ---------- DHT11 ----------
sensor = dht.DHT11(Pin(4))


# -------- LED --------
led = Pin(2, Pin.OUT)
led.value(0)


# ---------- WIFI CONNECT ----------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("WiFi connected")

#main change
TEMP_LIMIT = 27 #change freely for testing

# Track whether the user has enabled the relay with /on
manual_on = False

# Prevent repeated auto-OFF messages
auto_off_sent = False

def send_message(message):
    try:
        urequests.post(URL_SEND, json={
            "chat_id": CHAT_ID,
            "text": message
        }).close()
    except Exception as e:
        print("Send error:", e)
        
        
while True:
    try:
        # =========================
        # Read temperature/humidity
        # =========================
        sensor.measure()

        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temperature: {:.2f} °C".format(temp))
        print("Humidity: {:.2f} %".format(hum))
        print("Relay:", "ON" if led.value() else "OFF")


        # =========================
        # Check Telegram messages
        # =========================
        r = urequests.get(
            URL_GET + "?offset={}".format(last_id + 1)
        )

        data = r.json()
        r.close()

        messages = data["result"]

        for msg in messages:
            last_id = msg["update_id"]

            if "message" not in msg:
                continue

            if "text" not in msg["message"]:
                continue

            text = msg["message"]["text"]
            chat_id = msg["message"]["chat"]["id"]

            if str(chat_id) != CHAT_ID:
                continue


            # =========================
            # /on
            # =========================
            if text == "/on":
                led.value(1)

                manual_on = True
                auto_off_sent = False

                send_message("Relay ON - temperature control acknowledged")

                print("Telegram: /on")
                print("Relay ON")


            # =========================
            # /off
            # =========================
            elif text == "/off":
                led.value(0)

                manual_on = False

                send_message("Relay OFF")

                print("Telegram: /off")
                print("Relay OFF")


            # =========================
            # /status
            # =========================
            elif text == "/status":

                relay_state = "ON" if led.value() else "OFF"

                message = (
                    "Temperature: {:.2f} °C\n"
                    "Humidity: {:.2f} %\n"
                    "Relay: {}"
                ).format(temp, hum, relay_state)

                send_message(message)

                print("Status sent")


        # =========================
        # AUTOMATIC TEMPERATURE LOGIC
        # =========================

        if temp < TEMP_LIMIT:

            # Automatically turn relay OFF
            if led.value() == 1:
                led.value(0)
                manual_on = False

            # Send auto-OFF only once
            if not auto_off_sent:
                send_message(
                    "Auto-OFF: Temperature is below 25 °C. Relay OFF."
                )

                auto_off_sent = True

                print("Auto-OFF notification sent")


        elif temp >= TEMP_LIMIT:

            # Reset auto-OFF notification flag
            auto_off_sent = False

            # If relay is OFF and /on has NOT been received,
            # send alert every loop
            if led.value() == 0 and manual_on == False:

                send_message(
                    "ALERT: Temperature is {:.2f} °C. "
                    "Relay is OFF. Send /on to activate.".format(temp)
                )

                print("Temperature alert sent")


    except Exception as e:
        print("Error:", e)


    # =========================
    # Run every 5 seconds
    # =========================
    time.sleep(5)
