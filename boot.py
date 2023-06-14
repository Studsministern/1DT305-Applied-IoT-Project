# boot.py -- run on boot-up
from env import wifi as env
from lib.wifi import wifi_connect

# WiFi Connection
try:
    ip = wifi_connect(env.SSID, env.PASSWORD)
except KeyboardInterrupt:
    print('Keyboard interrupt')