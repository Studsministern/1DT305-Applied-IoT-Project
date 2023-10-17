from dht import DHT11
from machine import ADC, Pin
import utime as time
import env
from lib.wifi import WiFi
from lib.mqtt import MQTTClient


### SETUP ###
# LED and sensors
led = Pin("LED", Pin.OUT)  # The Raspberry Pi onboard LED
dht11 = DHT11(Pin(26))  # GP26 pin for measuring from the DHT11
soil_moisture_power = Pin(27, Pin.OUT)  # GP27 pin used to provide 3.3V VCC to the soil moisture sensor
soil_moisture_sensor = ADC(Pin(28))  # ADC2 pin for measuring from the FC28

# Making sure the soil moisture sensor is off when starting the program
soil_moisture_power.off()

# Creating a MQTT client variable
global mqttClient


### FUNCTIONS ###
def led_blink_once(half_delay):
    led.on()
    time.sleep(half_delay)
    led.off()
    time.sleep(half_delay)


def measure_dht11():
    dht11.measure()
    temperature = dht11.temperature()
    humidity = dht11.humidity()
    return temperature, humidity


def measure_fc28():
    soil_moisture_power.on()
    # Keeping the power for the soil moisture sensor on for a few seconds so a correct measurement is received
    time.sleep(2)
    moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
    soil_moisture_power.off()
    return moisturePercent


def mqtt_publish(mqtt_feed, data):
    print("Publishing: {0} to {1} ... ".format(data, mqtt_feed), end="")
    try:
        mqttClient.publish(topic=mqtt_feed, msg=str(data))
        print("DONE")
        led_blink_once(0.25)
    except Exception as e:
        print("FAILED", e)


def disconnect_all():
    try:
        # Making sure the soil moisture sensor does not stay on
        soil_moisture_power.off()

        # Disconnect MQTT Client and WiFi
        mqttClient.disconnect()
        print("\nDisconnected from Adafruit IO")

        WiFi.disconnect()
    except Exception as e:
        print("Error when disconnecting")


### LOOP ###
while True:
    try:
        # Connecting to WiFi
        WiFi.connect()

        # Blink when the WiFi is connected
        for i in range(0, 3):
            led_blink_once(0.05)

        # Connecting to MQTT broker
        print(f"Begin connection with MQTT Broker :: {env.AIO_BROKER}")
        mqttClient = MQTTClient(
            client_id=env.AIO_CLIENT_ID,
            server=env.AIO_BROKER,
            port=env.AIO_PORT,
            user=env.AIO_USERNAME,
            password=env.AIO_ACCESS_KEY,
        )
        mqttClient.connect()
        print(f"Connected to MQTT Broker :: {env.AIO_BROKER}\n")

        # Blink when connected to the MQTT Broker
        for i in range(0, 3):
            led_blink_once(0.05)

        # Measuring
        temperature, humidity = measure_dht11()
        moisturePercent = measure_fc28()

        print(
            f"Temperature is {temperature} degrees Celcius. Humidity is {humidity}%RH. Soil moisture is {int(moisturePercent)}%"
        )

        # Publishing
        mqtt_publish(env.AIO_FEED_TEMPERATURE, temperature)
        mqtt_publish(env.AIO_FEED_HUMIDITY, humidity)
        mqtt_publish(env.AIO_FEED_MOISTURE, moisturePercent)

        # Disconnecting and going to sleep
        disconnect_all()
        print(f"Going to sleep for {env.AIO_PUBLISH_INTERVAL} seconds ...")
        time.sleep(env.AIO_PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        # Disconnect and clean up if the user causes a KeyboardInterrupt
        disconnect_all()
        print("Keyboard interrupt")
        break
    except Exception as e:
        # Disconnect and try connecting again if another exception is thrown
        print("\nDid not manage to connect to WiFi or MQTT broker.")
        disconnect_all()
        print(f"Trying again in {env.WIFI_TRY_RECONNECT_INTERVAL} seconds.")
        time.sleep(env.WIFI_TRY_RECONNECT_INTERVAL)
