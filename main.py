from dht import DHT11
from machine import ADC, Pin
import utime as time
from lib.http import http_get_request

soil_moisture_sensor = ADC(Pin(26)) # Soil moisture sensor with ADC0 pin (GP26)
dht11 = DHT11(Pin(27))  # DHT11 Constructor with GP27 pin

# HTTP request
try:
    http_get_request('http://detectportal.firefox.com/')
except OSError as err:
    print(err)
    raise OSError('There may be something wrong with your WiFi connection. Check that you have a 2.4 GHz WiFi and correct credentials in env.py')
except Exception as err:
    raise err

while True:
    time.sleep(5)
    try:
        # Measuring soil moisture
        moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
        
        # Measuring air temperature and humidity
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()

        print(
            'Temperature is {} degrees Celsius. Humidity is {}%RH. Soil moisture is {}%'.format(
                temperature, humidity, int(moisturePercent)
            )
        )
    except Exception as err:
        print('An exception occured.' + str(err))
        continue
