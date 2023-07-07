import network
import env
from utime import sleep


class WiFi:
    def connect():
        wlan = network.WLAN(network.STA_IF)  # Find WLAN
        wlan.active(True)  # Activate network interface
        wlan.config(pm=0xA11140)  # set power mode to get WiFi power-saving off (if needed)

        print("\nConnecting to network...")
        wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)

        # Check if it is connected otherwise wait
        print("Waiting for connection...", end="")
        while not wlan.isconnected() and wlan.status() >= 0:
            print(".", end="")
            sleep(1)

        # Print the IP assigned by router
        ip = wlan.ifconfig()[0]

        # Check so the ip is not 0.0.0.0
        if ip is "0.0.0.0":
            wlan.disconnect()  # Disconnect if the connection is to the wrong WiFi
            wlan = None  # Cleanup
            raise Exception(
                "\nip = 0.0.0.0 - Not connected to WiFi. Check that you have a 2.4 GHz WiFi and correct credentials in env.py"
            )

        print(f"\nConnected on {ip}\n")

    def disconnect():
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan = None
        print("Disconnected from WiFi\n")
