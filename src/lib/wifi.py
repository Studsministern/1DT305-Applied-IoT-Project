import network
import env
from utime import sleep

def wifi_connect():
    # Disconnect from wlan
    wlan = network.WLAN(network.STA_IF)
    # Activate network interface
    wlan.active(True)
    # set power mode to get WiFi power-saving off (if needed)
    wlan.config(pm = 0xa11140)

    wlan.disconnect()

    print('\nConnecting to network...')
    wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)  # Your WiFi Credential

    # Check if it is connected otherwise wait
    print('Waiting for connection...', end='')
    while not wlan.isconnected() and wlan.status() >= 0:
        print('.', end='')
        sleep(1)
    print() # Print an empty line

    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]

    # Check so the ip is not 0.0.0.0
    if ip is '0.0.0.0':
        wlan.disconnect() # Disconnect if the connection is to the wrong WiFi
        wlan = None       # Cleanup
        raise Exception('ip = 0.0.0.0 - Not connected to WiFi. Check that you have a 2.4 GHz WiFi and correct credentials in env.py')
    
    print('Connected on {}\n'.format(ip))
    
def wifi_disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan = None
    print('Disconnected from WiFi\n')