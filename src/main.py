from dht import DHT11
from machine import ADC, Pin
import utime as time
import env
from lib.wifi import wifi_connect, wifi_is_connected, wifi_disconnect
from lib.mqtt import MQTTClient



### SENSORS SETUP ###
led = Pin("LED", Pin.OUT)
dht11 = DHT11(Pin(26))                 # DHT11 Constructor with GP26 pin
soil_moisture_power = Pin(27, Pin.OUT) # GP27 pin used to provide 3.3V VCC to the soil moisture sensor
soil_moisture_power.off()              # Making sure the soil moisture sensor is off when the program starts
soil_moisture_sensor = ADC(Pin(28))    # Soil moisture sensor with ADC2 pin (same pin as GP28)

# Blinking LED once to show on the board when trying to connect to WiFi, or when information is published
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

# Measuring soil moisture
def measure_fc28():
    try:
        soil_moisture_power.on()
        time.sleep(2) # Keeping the power for the soil moisture sensor on for a few seconds so a correct measurement is received
        moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
        soil_moisture_power.off()
        return moisturePercent
    except Exception as err:
        print('An exception occured when measuring soil moisture.' + str(err))



### MQTT SETUP ###
mqttClient = None
# Function to publish data to Adafruit IO MQTT server
def mqtt_publish(mqttClient, mqtt_feed, data):
    print('Publishing: {0} to {1} ... '.format(data, mqtt_feed), end='')
    try:
        mqttClient.publish(topic=mqtt_feed, msg=str(data))
        print('DONE')
        led_blink_once(0.25)
    except Exception as e:
        print('FAILED', e)



### DISCONNECTING ###
def disconnect_all(mqttClient):
    soil_moisture_power.off() # Making sure the soil moisture sensor does not stay on
    print()

    # Disconnecting the MQTT client
    try:
        mqttClient.disconnect()
        print('Disconnected from Adafruit IO')
        mqttClient = None
        print('MQTTClient cleaned up')
    except NameError as e:
        print('The mqttClient was not connected when trying to disconnect', e)

    wifi_disconnect()



### MAIN PROGRAM ###
try:
    while True:
        try:
            ### Connecting to WiFi ###
            wifi_connect()

            # Blink when the WiFi is connected
            for i in range(0, 3):
                led_blink_once(0.05)
            
            ### Connecting to MQTT broker
            print(f'Begin connection with MQTT Broker :: {env.MQTT_BROKER}')
            mqttClient = MQTTClient(client_id=env.MQTT_CLIENT_ID, server=env.MQTT_BROKER, port=env.MQTT_PORT, user=env.MQTT_USERNAME, password=env.MQTT_ACCESS_KEY)
            mqttClient.connect()
            print(f'Connected to MQTT Broker :: {env.MQTT_BROKER}\n')
            
            # Blink when connected to the MQTT Broker
            for i in range(0, 3):
                led_blink_once(0.05)
            
            ### Measuring ###
            temperature, humidity = measure_dht11()
            moisturePercent = measure_fc28()

            print(
                'Temperature is {} degrees Celsius. Humidity is {}%RH. Soil moisture is {}%'.format(
                    temperature, humidity, int(moisturePercent)
                )
            )

            ### Publishing ###
            try:
                mqtt_publish(mqttClient, env.MQTT_FEED_TEMPERATURE, temperature)
                mqtt_publish(mqttClient, env.MQTT_FEED_HUMIDITY, humidity)
                mqtt_publish(mqttClient, env.MQTT_FEED_MOISTURE, moisturePercent)
            except:
                print(f'Something went wrong when publishing. Connecting again in {env.WIFI_TRY_RECONNECT_INTERVAL} seconds.')
                time.sleep(env.WIFI_TRY_RECONNECT_INTERVAL)
                continue

            ### Disconnecting and going to sleep ###
            disconnect_all(mqttClient)
            print(f'Going to sleep for {env.MQTT_PUBLISH_INTERVAL} seconds ...')
            time.sleep(env.MQTT_PUBLISH_INTERVAL)
        except KeyboardInterrupt:
            print('Keyboard interrupt')
            break
        except Exception as e:
            print(f'Did not manage to connect to WiFi or broker. Trying again in {env.WIFI_TRY_RECONNECT_INTERVAL} seconds.')
            time.sleep(env.WIFI_TRY_RECONNECT_INTERVAL)
finally:
    # Disconnect and clean up if an exception is thrown when publishing
    disconnect_all(mqttClient)