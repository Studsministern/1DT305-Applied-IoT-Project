from dht import DHT11
from machine import ADC, Pin
import utime as time
import env
from lib.wifi import wifi_connect, wifi_is_connected
from lib.mqtt import MQTTClient



### SENSOR SETUP ###
soil_moisture_sensor = ADC(Pin(26)) # Soil moisture sensor with ADC0 pin (GP26)
dht11 = DHT11(Pin(27))  # DHT11 Constructor with GP27 pin
led = Pin("LED", Pin.OUT)

# Blinking LED once to show on the board when information is sent
def led_blink_once(half_delay):
    led.on()
    time.sleep(half_delay)
    led.off()
    time.sleep(half_delay)

# Measuring air temperature and humidity
def measure_dht11():
    try:
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()
        return temperature, humidity
    except Exception as err:
        print('An exception occured when measuring temperature and humidity.' + str(err))

def measure_fc28():
    try:
        # Measuring soil moisture
        moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
        return moisturePercent
    except Exception as err:
        print('An exception occured when measuring soil moisture.' + str(err))



### MQTT SETUP ###
# Function to publish data to Adafruit IO MQTT server
def mqtt_publish(mqttClient, feed_ending, data):
    full_topic = env.MQTT_FEED + feed_ending
    print('Publishing: {0} to {1} ... '.format(data, full_topic), end='')
    try:
        mqttClient.publish(topic=full_topic, msg=str(data))
        print('DONE')
        led_blink_once(0.25)
    except Exception as e:
        print('FAILED', e)



### Connecting to WiFi and MQTTClient ###
mqttClient = None
try:
    while True:
        try:
            for i in range(0, 3):
                led_blink_once(0.1)
            wifi_connect()
            # Use the MQTT protocol to connect to Adafruit IO
            print(f'Begin connection with MQTT Broker :: {env.MQTT_BROKER}')
            mqttClient = MQTTClient(client_id=env.MQTT_CLIENT_ID, server=env.MQTT_BROKER, port=env.MQTT_PORT, user=env.MQTT_USERNAME, password=env.MQTT_ACCESS_KEY, keepalive=60)
            mqttClient.connect()
            print(f'Connected to MQTT Broker :: {env.MQTT_BROKER}')
            led.off()
            
            ### MAIN LOOP ###
            while True:
                time.sleep(env.MQTT_PUBLISH_INTERVAL)
                temperature, humidity = measure_dht11()
                moisturePercent = measure_fc28()

                print(
                    'Temperature is {} degrees Celsius. Humidity is {}%RH. Soil moisture is {}%'.format(
                        temperature, humidity, int(moisturePercent)
                    )
                )

                if wifi_is_connected():
                    mqtt_publish(mqttClient, '.dht11-temperature', temperature)
                    mqtt_publish(mqttClient, '.dht11-humidity', humidity)
                    mqtt_publish(mqttClient, '.fc28-humidity', moisturePercent)
                else:
                    print(f'WiFi not connected when publishing. Connecting again.')
                    break
        except KeyboardInterrupt:
            print('Keyboard interrupt')
            break
        except Exception as e:
            print(f'Did not manage to connect to broker. Trying again.')
        time.sleep(5)
finally:
    # Disconnect and clean up if an exception is thrown when publishing
    try:
        mqttClient.disconnect()
        mqttClient = None
        print('Disconnected from Adafruit IO')
    except NameError as e:
        print('The mqttClient didn\'t manage to connect')