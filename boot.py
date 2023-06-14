# boot.py -- run on boot-up
import env
from lib.wifi import wifi_connect

# WiFi Connection
try:
    ip = wifi_connect(env.WIFI_SSID, env.WIFI_PASSWORD)
except KeyboardInterrupt:
    print('Keyboard interrupt')