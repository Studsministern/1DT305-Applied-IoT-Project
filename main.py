from dht import DHT11
from machine import ADC, Pin
import utime as time
import env
from lib.mqtt import MQTTClient



### MQTT ###
# Use the MQTT protocol to connect to Adafruit IO
print(f'Begin connection with MQTT Broker :: {env.MQTT_BROKER}')
mqttClient = MQTTClient(env.MQTT_CLIENT_ID, env.MQTT_BROKER, env.MQTT_PORT, env.MQTT_USERNAME, env.MQTT_ACCESS_KEY)
mqttClient.connect()
print(f'Connected to MQTT Broker :: {env.MQTT_BROKER}')

# Function to publish data to Adafruit IO MQTT server
def mqtt_publish(data):
    global last_publish

    print('Publishing: {0} to {1} ... '.format(data, env.MQTT_FEED), end='')
    try:
        mqttClient.publish(topic=env.MQTT_FEED, msg=str(data))
        print('DONE')
    except Exception as e:
        print('FAILED', e)



### SENSOR SETUP ###
soil_moisture_sensor = ADC(Pin(26)) # Soil moisture sensor with ADC0 pin (GP26)
dht11 = DHT11(Pin(27))  # DHT11 Constructor with GP27 pin



# Loop
try:
    while True:
        time.sleep(env.MQTT_PUBLISH_INTERVAL)

        try:
            # Measuring soil moisture
            moisturePercent = 0 #100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
            
            # Measuring air temperature and humidity
            dht11.measure()
            temperature = dht11.temperature()
            humidity = dht11.humidity()
        except Exception as err:
            print('An exception occured.' + str(err))
            continue

        print(
            'Temperature is {} degrees Celsius. Humidity is {}%RH. Soil moisture is {}%'.format(
                temperature, humidity, int(moisturePercent)
            )
        )

        mqtt_publish(temperature)
finally: # Disconnect and clean up if an exception is thrown when publishing
    mqttClient.disconnect()
    mqttClient = None
    print('Disconnected from Adafruit IO')