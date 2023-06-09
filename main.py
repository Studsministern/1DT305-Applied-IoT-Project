from dht import DHT11
from machine import Pin
import utime as time

dht11 = DHT11(Pin(27))  # DHT11 Constructor with GP27 pin

while True:
    time.sleep(5)
    try:
        dht11.measure()  # Measuring values from the sensor

        t = dht11.temperature()  # Getting the temperature in degrees Celcius
        h = dht11.humidity()  # Getting the humidity in %RH (Relative Humidity)

        print(
            "Temperature is {} degrees Celsius and Humidity is {}%".format(
                temperature, humidity
            )
        )

    except:
        print("An exception occured.")
        continue
