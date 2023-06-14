# boot.py -- run on boot-up
from lib.wifi import wifi_connect

# WiFi Connection
try:
    ip = wifi_connect()
except KeyboardInterrupt:
    print('Keyboard interrupt')