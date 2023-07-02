# Indoor plant monitoring with a RP2

## Introduction

My name is Eric Weidow and I am an Electrical Engineering student at LTH in Lund, Sweden. As I wanted more practical experience with electronics and programming, I signed up for a summer course in Applied IoT a Linnaeus University (student credentials: ew223me), Sweden, and this project is part of that course.

The project is made up of a Raspberry Pi Pico WH (henceforth called **RP2**) with two sensors to measure air temperature, air humidity, and the soil moisture for an indoor plant. The data is sent via Wi-Fi to [Adafruit IO](https://io.adafruit.com/) (AIO) using the MQTT protocol. The data is stored in the Adafruit IO account and displayed using a dashboard.

The goal of this project is being able to visualize the soil moisture for an indoor plant, and notify the user when the plant should be watered. As both air temperature and air humidity is measured, I hope to see some connection between, for example, air humidity and how quickly the soil moisture decreases. I will use this IoT device as a way for reminding me when to water my plants, as I have always been bad at taking care of them. Additionally, it will give me a great amount of experience with IoT, microcontrollers, sensors, Python, and much more!

In total, it should take about 3-4 hours to complete the project if this tutorial is followed.



&nbsp;

## Tutorial

### Materials

The materials used in this project are shown in Table 1, below:

<div align="center">
    <h6>
        <b>Table 1</b>. The material list. Costs, links images for each product are included. Data received from the <a href="https://www.electrokit.com/">Electrokit</a> website.
    </h6>

| Material                               | Cost    | Link                                                                                                     | Image                                                    |
| -------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Raspberry Pi Pico WH                   | 109 SEK | <a href="https://www.electrokit.com/produkt/raspberry-pi-pico-wh/">here</a>                              | <img src="img/Raspberry Pi Pico WH.jpg" width=150>       |
| DHT11 Temperature & Humidity Sensor    | 49 SEK  | <a href="https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/">here</a>           | <img src="img/DHT11 Sensor.jpg" width=150>               |
| FC-28 Soil Moisture Sensor             | 29 SEK  | <a href="https://www.electrokit.com/produkt/jordfuktighetssensor/">here</a>                              | <img src="img/FC-28 Soil Moisture Sensor.jpg" width=150> |
| Breadboard (a smaller size works fine) | 69 SEK  | <a href="https://www.electrokit.com/produkt/kopplingsdack-840-anslutningar/">here</a>                    | <img src="img/Breadboard.jpg" width=150>                 |
| Wires (at least 6 male-male)           | 39 SEK  | <a href="https://www.electrokit.com/produkt/kopplingstrad-byglar-for-kopplingsdack-mjuka-65st/">here</a> | <img src="img/Wires.jpg" width=150>                      |

</div>

#### DHT11 Temperature & Humidity Sensor

The DHT11 Temperature & Humidity Sensor is a cheap but reliable sensor with a digital signal output, which requires a supply voltage V<sub>CC</sub> of 3.3-5 V. Measurement specifications are included in Table 2, below.

<div align="center">
    <h6>
        <b>Table 2</b>. RH = Relative Humidity, the amount of vapor present in air expressed as a percentage (%RH) of what is required to achieve saturation at the same temperature. Data received from the <a href="https://www.electrokit.com/uploads/productfile/41015/DHT11.pdf">DHT11 datasheet</a> on the <a href="https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/">DHT11 product page</a>.
    </h6>

| Measurement Range | Humidity Accuracy | Temperature Accuracy | Resolution            |
| ----------------- | ----------------- | -------------------- | --------------------- |
| 20-90%RH          | &plusmn;5%RH      | &plusmn;2 &deg;C     | Humidity: 1%RH        |
| 0-50 &deg;C       |                   |                      | Temperature: 1 &deg;C |

</div>

Datasheets recommended not sending instructions to the sensor in within one second of supplying power to it, to pass the unstable status. If, for example, WiFi and a MQTT Broker is connected before taking measurements, this is not a problem.

#### FC-28 Soil Moisture Sensor

The FC-28 Soil Moisture Sensor measures resistance between two exposed pads. The resistance is converted to a voltage between 0 and V<sub>CC</sub>, which can be measured by a microcontroller. The voltage can then be used to determine the moisture of the soil. The sensor requires an input voltage V<sub>CC</sub> of 3.3-5 V. The voltage measured by the sensor is available on two different pinouts:

- The `AO` (Analog output) pinout can be measured to get an analog voltage with a value between 0 and V<sub>CC</sub>.
- The `DO` (Digital output) pinout can be measured to get either 0 (`LOW`) or V<sub>CC</sub> (`HIGH`). The sensor has a chip with a comparator and a variable resistor. By rotating the variable resistor, it can be decided at what analog voltage the `DO` pinout should be set to either `LOW` or `HIGH`.

The [online user guide](https://www.electrokit.com/uploads/productfile/41015/41015738_-_Soil_Moisture_Sensor.pdf) supplied by Electrokit on the product page, says:

> "As the probe passes current through the soil, it carries ions that will damage the surface layer over time. As such the sensor should not be operated permanently. Instead it should only be powered up when a measurement is taken and then instantly shut down again."

Therefore the sensor should only ever be on for a few seconds before taking measurements. 



&nbsp;

### Computer setup

Make sure to go through every step of this setup so you don't miss downloading or installing anything.

<details>
    <summary><b>1. Setting up the IDE</b></summary></br>
    
For the IDE I chose VSCode. The steps to setup VSCode for Windows with the correct extension (Pymakr) are the following:

1. Download and install the LTS release of Node.js [from this link](https://nodejs.org/en).
2. Download and install VSCode [from this link](https://code.visualstudio.com/Download).
3. Open VSCode.
4. Open the **Extensions manager** from the left panel icon _OR_ press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd>.
5. Search for the **Pymakr** extension and install it.
</details>

<details>
    <summary><b>2. Flashing firmware to the RP2</b></summary></br>

With the IDE installed, the firmware now needs to be flashed to the RP2. Make sure you have your RP2 and cable for these steps:

1. Download the micropython firmware [from this link](https://micropython.org/download/rp2-pico-w/). Make sure that you download the latest firmware from `Releases`, and **not** from `Nightly builds`. You will get a `.uf2` file.
2. Connect the **micro-usb** end of the cable to the RP2. Firmly hold the back of the USB slot when connecting the cable. There will probably be a small gap even when fully inserted, this is normal.
3. While holding the <kbd>BOOTSEL</kbd> button on the RP2, connect the **USB type A** end of the cable to your computer. When you have connected the cable you can release the <kbd>BOOTSEL</kbd> button.
4. There should be a new drive on your file system named `RPI-RP2`. This is the RP2 storage. Copy the `.uf2` file you downloaded earlier into this storage. **Do not disconnect the device during this installation! If you do you will most likely need to redo the above steps of flashing the firmware.**
5. Your RP2 should now automatically disconnect and reconnect.
</details>

<details>
    <summary><b>3. Cloning and configuring the code from this repository</b></summary></br>
        
All code for this project is availible in this GitHub repository. Follow the steps below:

1. Find a place where you want to clone the code to. A folder will automatically be created when cloning code. But create a parent folder if you want to.
2. In VSCode, press <kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd> to open the editor commands.
3. Write `Git: Clone` and choose `Git: Clone` when it shows up.
4. In the field which says `Provide repository URL or pick a repository source.`, copy and paste `https://github.com/Studsministern/1DT305-Applied-IoT-Project`. Press <kbd>ENTER</kbd>.
5. Navigate to where you want the folder with code to be cloned to. Press <kbd>Select as Repository Destination</kbd>.
6. When it has finished cloding, a window saying "Would you like to open the cloned repository, or add it to the current workspace?" will show up. Press <kbd>Open</kbd>.
7. Create a file called `env.py` and copy the contents of `env.py.example` into it. Then change the variable values to your WiFi credentials, MQTT variables, etc.

</details>

<details>
    <summary><b>4. Uploading the code to the RP2</b></summary></br>
    
Make sure the RP2 is connected to the computer. To upload the code to the RP2, you should already have the IDE installed and the firmware flashed. Then upload the code by following these steps:

1. In VSCode, open **Pymakr** from the left panel icon. Find the device and press `Connect device` (a small lightning symbol) and `Create terminal` (a box with a right arrow).
2. Find `PYMAKR: PROJECTS` in either **Pymakr** or **Explorer** on the left panel.
3. Press <kbd>ADD DEVICES</kbd> and select the device.
4. Press `Sync project to device` (a cloud with an upwards arrow).
5. If you want the file contents to automatically update as you do changes, find `PYMAKR: PROJECTS` again. Hold your mouse over the project. Press <kbd></></kbd> (`Start development mode`).
</details>



&nbsp;

### Putting everything together

#### Circuit diagram

The circuit diagram shows how the microcontroller is connected to the sensors. All wires are male-male except for the wires between the FC-28 chip and probe, which are female-female wires and were included with the FC-28.

<div align="center">
    <img src="img/PicoW Indoor plant monitoring_bb.jpg">
    <h6>
        <b>Figure 1</b>. A circuit diagram identical to the real circuit. The circuit contains a Raspberry Pi Pico WH (left), a DHT11 sensor (middle) and a FC-28 sensor (right) connected with wires Diagram made in <a href="https://fritzing.org/">Fritzing</a> version 0.9.3b.
    </h6>
</div>

#### DHT11
A voltage of V<sub>CC</sub> = 3.3 V was chosen for powering the DHT11. The power is connected to the middle leg of the DHT11 and is supplied by pin 36 (`3V3(OUT)`) on the RP2. The signal pin (the left leg as seen in the circuit diagram) on the DHT11 is connected to pin 31 (`GP26`) on the RP2 to take measurements. The version of the DHT11 bought from Electrokit has a built-in 10 k&Omega; pullup resistor, so no extra resistors are needed in the circuit.

#### FC-28

A supply voltage of V<sub>CC</sub> = 3.3 V was chosen for the FC-28 as well. However, the `3V3(OUT)` pin is not used. As mentioned in the materials section, keeping the sensor powered on will damage it. Instead I investigated using a GPIO to supply power to the sensor:

When suppying power with the `3V3(OUT)` pin, I was able to measure that the V<sub>CC</sub> pin on the sensor received a current of 2.9 mA, by using a multimeter. There does not appear to be any official documentation of how much current a GPIO pin is allowed to use. However, discussions in many forums suggest 16 mA to be the absolute max current from any one pin, and that the GPIO pins were designed for a current draw of at least 3 mA.

Therefore I used pin 32 (`GP27`) as a digital output pin to provide the supply voltage to the FC-28. The sensor is only ever kept on for 2 seconds before each measurement. I am unsure if this is the best value to use when taking both the lifetime of the sensor and the accuracy of the measurements into account. But it seems to produce quite stable values.

The measurement is done with pin 34 (`ADC2`), which is connected to the `AO` pinout on the FC-28. The ADC (Analog-Digital Converter) in the RP2 converts the 0-3.3 V voltage to a 16-bit number, between 0 and 65535. 0 corresponds to very low resistance (high moisture) and 65535 corresponds to very high resistance (low moisture). The read value is translated to a moisture percentage using the following equation:

&nbsp;

```math
\text{Moisture percentage} = 100 - \frac{\text{read value} \cdot 100}{65535}$$
```

With the code equivalent:

```python
    moisturePercent = 100 - (soil_moisture_sensor.read_u16() / 65535 * 100)
```



&nbsp;

### Platform

The platform chosen for this project is [Adafruit IO](https://io.adafruit.com/) (AIO). It is very simple to setup, and also offers the option of building dashboards. It has a free tier which allows up to 2 devices, 5 groups, 10 feeds, 5 dashboards, a data rate of 30 messages per minute, and also provides 30 days storage. This project only needs 1 group, 3 feeds, 1 dashboard and a very low data rate, which means the free tier works perfect.

To use the platform, it is required to make an account. Then a group with three feeds need to be setup: one feed for the DHT11 temperature values, one for the DHT11 humidity values and one for the FC-28 soil moisture values. Adafruit IO has great [basics tutorials](https://learn.adafruit.com/search?q=Adafruit%2520IO%2520Basics) to help with these steps.



&nbsp;

### The code

The file structure is:

```graphql
boot.py          - # Runs on startup
main.py          - # Runs when boot is completed
env.py           - # Containing environment variables
env.py.example   - # Example for environment variables
lib/*            - # Library files
├─ __init.py__   - # Init file to allow importing from lib
├─ mqtt.py       - # Library for creating an MQTTClient
└─ wifi.py       - # Handling connection to WiFi
pymakr.conf      - # Pymakr configuration file
```

`boot.py` runs on startup, but does not contain any code in this project.

`main.py` is where most of the code is. It contains all setup and measuring of sensors. It uses functions from `lib/wifi.py` to connect to and disconnect from WiFi, and functions from `lib/mqtt.py` to connect to, publish to and disconnect from AIO.

The program itself is in a very long loop, which looks very complicated. However, it is actually quite simple. The first step of the loop is connecting to WiFi and the MQTT Broker (AIO). The onboard LED blinks three times after connecting to WiFi, and three times after connecting to the MQTT broker:

https://github.com/Studsministern/1DT305-Applied-IoT-Project/blob/1c357c3f17382f9b52a02110dce34a8df8242877/src/main.py#L82-L98

When the WiFi connection and MQTT connection are setup, values are measured from the sensors and printed to the console:

https://github.com/Studsministern/1DT305-Applied-IoT-Project/blob/1c357c3f17382f9b52a02110dce34a8df8242877/src/main.py#L99-L108

After measuring, the values are published to AIO. The onboard LED will blink once for each successful publishing:

https://github.com/Studsministern/1DT305-Applied-IoT-Project/blob/1c357c3f17382f9b52a02110dce34a8df8242877/src/main.py#L109-L118

If we have gotten this far without an exception being thrown, we are done with the publishing! We now want the RP2 to sleep (set with `MQTT_PUBLISH_INTERVAL`, default is 20 minutes). But before going to sleep, we disconnect the RP2 from WiFi and AIO, and turn off the soil moisture sensor's power, using the `disconnect_all` function:

https://github.com/Studsministern/1DT305-Applied-IoT-Project/blob/1c357c3f17382f9b52a02110dce34a8df8242877/src/main.py#L119-L122

After the RP2 wakes up, it will start at the beginning of the loop, and continue publishing every `MQTT_PUBLISH_INTERVAL` seconds! However, if an exception is thrown at any moment, the RP2 will sleeps (set with `WIFI_TRY_RECONNECT_INTERVAL`, default is 1 minute) and then the loop starts over. Because of this, a temporary loss of WiFi will be solved by itself.

The only way of exiting the loop is by a KeyboardInterrupt, then the WiFi and MQTT Broker is disconnected, and the soil moisture sensor's power is turned off, before the RP2 stops the program:

https://github.com/Studsministern/1DT305-Applied-IoT-Project/blob/1c357c3f17382f9b52a02110dce34a8df8242877/src/main.py#L123-L127

The sleep times `MQTT_PUBLISH_INTERVAL` and `WIFI_TRY_RECONNECT_INTERVAL`, along with all other environment variables, are set in `env.py`. The file has to be created by the user and should contain all variables from the file `env.py.example`, but with the values changed to the corresponding usernames, password, keys, etcetera:

```python
# WiFi configuration
WIFI_SSID = 'Your_WiFi_SSID'                                    # WiFi SSID (name)
WIFI_PASSWORD = 'Your_WiFi_password'                            # WiFi password
WIFI_TRY_RECONNECT_INTERVAL = 60                                # Time interval before trying to connect to WiFi again


# Adafruit IO configuation
MQTT_BROKER = 'io.adafruit.com'                                 # MQTT broker IP address or DNS
MQTT_PORT = 1883                                                # Port for MQTT message
MQTT_USERNAME = 'Your_Username'                                 # Adafruit username
MQTT_ACCESS_KEY = 'Your_Access_Key'                             # Adafruit access key (something like aio_lotsofnumbersandletters)
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())         # The Pico W unique ID
MQTT_PUBLISH_INTERVAL = 1200                                    # Time interval between measuring and publishing, in seconds. Right now set to 20 minutes
MQTT_FEED_TEMPERATURE = 'Your_Username/f/Your_Temperature_Feed' # Feed for temperature (something like Your_Username/f/picow.dht11-temperature)
MQTT_FEED_HUMIDITY = 'Your_Username/f/Your_Humidity_Feed'       # Feed for humidity (something like Your_Username/f/picow.dht11-humidity)
MQTT_FEED_MOISTURE = 'Your_Username/f/Your_Moisture_Feed'       # Feed for soil moisture (something like Your_Username/f/picow.fc28-moisture)
```

Finally we have the files in the library folder (`lib/*`):
- `__init.py__` has to be in the `lib` folder to be able to import `mqtt.py` and `wifi.py` from `main.py`.
- `mqtt.py` contains functions to create a MQTT connection. It was provided by Linnaeus University from their [Applied IoT GitHub repository](https://github.com/iot-lnu/applied-iot/blob/master/Raspberry%20Pi%20Pico%20(W)%20Micropython/network-examples/N2_WiFi_MQTT_Webhook_Adafruit/lib/mqtt.py).
- `wifi.py` contains functions that connects to and disconnects from WiFi.



&nbsp;

### Transmitting the data / connectivity

<!--
How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

- [ ] How often is the data sent?
- [ ] Which wireless protocols did you use (WiFi, LoRa, etc ...)?
- [ ] Which transport protocols were used (MQTT, webhook, etc ...)
- [ ] \*Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.
-->



&nbsp;

### Presenting the data

<!--
Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

- [ ] Provide visual examples on how the dashboard looks. Pictures needed.
- [ ] How often is data saved in the database.
- [ ] \*Explain your choice of database.
- [ ] \*Automation/triggers of the data.
-->



&nbsp;

### Finalizing the design

#### Final design

#### Conclusion
The code is very forgiving, as it will continue trying to reconnect to WiFi and MQTT brokers until it succeeds, and because it will automatically disconnect from WiFi and the MQTT broker before going to sleep. The circuitry is also extremely simple, as it doesn't require any extra components other than the microcontroller and the sensors themselves. Because of how the code and circuitry turned out, I am very satisfied with this project. It has taught me a lot, and I believe it provides a great starting point for further development.

#### Further improvements
Some suggestions for improvements are:
- Connecting all electronics on a small experimental board or custom made PCB, and 3D-print a case for it. The FC-28 sensor probe and the micro-USB cable would then be connected to this case.
- Using batteries for power.
- Using subscription to be able to change delays or other settings from a dashboard.
- Using the soil moisture information to automatically trigger watering of plants.

<!--
Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

- [ ] Show final results of the project
- [ ] Pictures
- [ ] \*Video presentation
-->



&nbsp;

---

## Useful links

- [DHT11 sensor example for RP2](<https://github.com/iot-lnu/applied-iot/tree/master/Raspberry%20Pi%20Pico%20(W)%20Micropython/sensor-examples/P5_DHT_11_DHT_22>)
- [FC-28 sensor example for Arduino](https://lastminuteengineers.com/soil-moisture-sensor-arduino-tutorial/)
- [Measuring from the analog pins on RP2](https://pycopy.readthedocs.io/en/latest/rp2/quickref.html#adc-analog-to-digital-conversion)
