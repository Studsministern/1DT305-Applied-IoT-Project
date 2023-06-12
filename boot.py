# boot.py -- run on boot-up
from lib.env import get_env
from lib.wifi import wifi_connect

env = get_env()

# WiFi Connection
try:
    ip = wifi_connect(env['SSID'], env['PASSWORD'])
except KeyboardInterrupt:
    print('Keyboard interrupt')