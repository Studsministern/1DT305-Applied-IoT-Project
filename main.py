from dht import DHT11
from machine import ADC, Pin
import utime as time

soil_moisture_sensor = ADC(Pin(26)) # Soil moisture sensor with ADC0 pin (GP26)
dht11 = DHT11(Pin(27))  # DHT11 Constructor with GP27 pin

# TODO: Make the raspberry pi sleep instead of always being active. This both saves battery and makes the soil moisture sensor last longer.

while True:
    time.sleep(5)
    try:
        # TODO: Test to see what values correspond to the plant being dry and what values correspond to the plant being recently watered.
        # In the first test read_u16() gave a value of 47000 for dry soil and 22000 while being watered. Limits of 65535 and 0 may not correspond to 0 and 100 % moisture 

        # Measuring soil moisture
        moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
        
        # Measuring air temperature and humidity
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()

        print(
            "Temperature is {} degrees Celsius. Humidity is {}%RH. Soil moisture is {}%".format(
                temperature, humidity, int(moisture)
            )
        )
    except:
        print("An exception occured.")
        continue
