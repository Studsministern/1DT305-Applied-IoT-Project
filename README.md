# 1DT305-Applied-IoT-Project

## Introduction

My name is Eric Weidow and I am an Electrical Engineering student at LTH in Lund, Sweden. As I wanted more practical experience with electronics and programming, I signed up for a summer course in Applied IoT a Linnaeus University (student credentials: ew223me), Sweden, and this project is part of that course.

The project is made up of a Raspberry Pi Pico WH (henceforth called **RP2**) with two sensors to measure air temperature, air humidity, and the soil moisture for an indoor plant. The data is sent via Wi-Fi to a backend, where the data is stored. A dashboard is then used to display the stored data to the user.

> TBD: Storage solution, vizualisation solution, approximate build time. 

The goal of this project is being able to visualize and predict the soil humidity for an indoor plant, and notify the user when the plant should be watered. As both air temperature and air humidity is measured, the goal is that the prediction of when the plant needs to be watered can be improved based on this data. I will use this IoT device as a way for reminding me when to water my plants, as I have always been bad at taking care of them. Additionally, it will give me a great amount of experience with:
- Microcontrollers
- Sensors
- Communication between microcontrollers and sensors
- IoT concepts and principles
- Network protocols
- Cloud storage solutions
- Creating dashboards
- _...and much more!_

<!--
Give a short and brief overview of what your project is about.
What needs to be included:

- [ ] Title
- [x] Your name and student credentials (xx666x)
- [x] Short project overview
- [ ] How much time it might take to do (approximation)
-->

<!--
Describe why you have chosen to build this specific device. What purpose does it serve? What do you want to do with the data, and what new insights do you think it will give?

- [x] Why you chose the project
- [x] What purpose does it serve
- [x] What insights you think it will give

-->

&nbsp;

## Tutorial

<!-- Please keep the total length of the tutorial below 25k characters. You can include code that is linked to a repository. Keep the code snippets in the tutorial short. -->

### Materials

<!--
The materials used in this project, along with costs (in SEK) and links to a Swedish reseller, are the following:

| Material             | Cost              | Link |
| -------------------- | ----------------- |      |
| Raspberry Pi Pico WH |                   |      |
|                      |                   |      |

The Raspberry Pi Pico W will henceforth be called the RP2, which is a common notation for a Raspberry Pi with a 2040 chip.
-->

<!--
> Explain all material that is needed. All sensors, where you bought them and their specifications. Please also provide pictures of what you have bought and what you are using.
>
> - [ ] List of material
> - [ ] What the different things (sensors, wires, controllers) do - short specifications
> - [ ] Where you bought them and how much they cost
>
> Example: In this project I have chosen to work with the Pycom LoPy4 device as seen in Fig. 1, it's a neat little device programmed by MicroPython and has several bands of connectivity. The device has many digital and analog input and outputs and is well suited for an IoT project.
>
> ![LoPy!](https://pycom.io/wp-content/uploads/2018/08/lopySide-1.png =360x)
> Fig. 1. LoPy4 with headers. Pycom.io

-->

#### DHT11 Temperature & Humidity Sensor

The DHT11 Temperature & Humidity Sensor is a cheap but reliable sensor with a digital signal output. The sensor is manufactured by Elegoo can be bought for 49 SEK [here, from electrokit.com](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/).

Different datasheets showed different recommended voltages, from 3.3 V to 5 V. Testing showed that a V<sub>dd</sub> voltage of 3.3 V works very well. In this project V<sub>dd</sub> is supplied by pin 36 (`3V3(OUT)`) on the RP2. The Elegoo manufactured DHT11 includes a 10 k&Omega; pullup resistor, which means no extra resistor is needed in the circuit. Measurement specifications are included in Table 1, below.

<div align="center">
        <h6>
            <b>Table 1</b>. RH = Relative Humidity, the amount of vapor present in air expressed as a percentage (%RH) of what is required to achieve saturation at the same temperature. Data received from the <a href="https://www.electrokit.com/uploads/productfile/41015/DHT11.pdf">DHT11 datasheet</a> on the <a href="https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/">DHT11 product page</a>.
        </h6>

| Measurement Range | Humidity Accuracy | Temperature Accuracy | Resolution            |
| ----------------- | ----------------- | -------------------- | --------------------- |
| 20-90%RH          | &plusmn;5%RH      | &plusmn;2 &deg;C     | Temperature: 1 &deg;C |
| 0-50 &deg;C       |                   |                      | Humidity: 1%RH        |
          
</div>

<!-- From data sheet: DHT11’s power supply is 3-5.5V DC. When power is supplied to the sensor, do not send any instruction to the sensor in within one second in order to pass the unstable status. One capacitor valued 100nF can be added between VDD and GND for power filtering. -->

&nbsp;

#### FC-28 Soil Moisture Sensor

The FC-28 Soil Moisture Sensor measures the resistance between the two exposed pads. This is converted to a voltage (0 to V<sub>CC</sub>) which can be measured by a microcontroller to determine the moisture of the soil. The sensor can be bought for 29 SEK [here, from electrokit.com](https://www.electrokit.com/produkt/jordfuktighetssensor/).

The sensor requires an input voltage V<sub>CC</sub> of 3.3-5 V. In this project V<sub>CC</sub> = 3.3 V by supplying voltage from pin 36 (`3V3(OUT)`) on the RP2. The voltage measured by the sensor is availible on two different pinouts:

- The `AO` (Analog output) pinout can be measured to get the sensor's analog voltage of 0 to V<sub>CC</sub>.
- The `DO` (Digital output) pinout can be measured to get either 0 (`LOW`) or V<sub>CC</sub> (`HIGH`). The sensor has a comparator and a variable resistor on a chip. The voltage measured by the sensor is compared to the voltage produced using the variable resistor, which then sets the `DO` pinout to either `LOW` or `HIGH`.

In this project the `AO` pinout is used. The ADC (Analog-Digital Converter) on the RP2 pin converts the 0-3.3 V to a 16-bit number, between 0 and 65535. 0 corresponds to very low resistance (high moisture) and 65535 corresponds to very high resistance (low moisture).

&nbsp;

### Computer setup

<!--
How is the device programmed. Which IDE are you using. Describe all steps from flashing the firmware, installing plugins in your favorite editor. How flashing is done on MicroPython. The aim is that a beginner should be able to understand.

- [ ] Chosen IDE
- [ ] How the code is uploaded
- [ ] Steps that you needed to do for your computer. Installation of Node.js, extra drivers, etc.

-->

### Putting everything together

<!--
How is all the electronics connected? Describe all the wiring, good if you can show a circuit diagram. Be specific on how to connect everything, and what to think of in terms of resistors, current and voltage. Is this only for a development setup or could it be used in production?

- [ ] Circuit diagram (can be hand drawn)
- [ ] \*Electrical calculations
-->

### Platform

<!--
Describe your choice of platform. If you have tried different platforms it can be good to provide a comparison.

Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free? Describe the different alternatives on going forward if you want to scale your idea.

- [ ] Describe platform in terms of functionality
- [ ] \*Explain and elaborate what made you choose this platform
-->

### The code

<!--
Import core functions of your code here, and don't forget to explain what you have done! Do not put too much code here, focus on the core functionalities. Have you done a specific function that does a calculation, or are you using clever function for sending data on two networks? Or, are you checking if the value is reasonable etc. Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.

```python=
import this as that

def my_cool_function():
    print('not much here')

s.send(package)

# Explain your code!
```
-->

The file structure is:

```graphql
boot.py - # Runs on startup
main.py - # Runs when boot is completed
pymakr.conf - # Micropython configuration file
```

<!--
lib/* - # Library files
├─ example - # example file
├─ lib/folder/* - # example folder in library
│  ├─ example - # example file in folder
│  └─ Everything else... - # everything else, should not be needed
└─ example - # example file
-->

### Transmitting the data / connectivity

<!--
How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

- [ ] How often is the data sent?
- [ ] Which wireless protocols did you use (WiFi, LoRa, etc ...)?
- [ ] Which transport protocols were used (MQTT, webhook, etc ...)
- [ ] \*Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.
-->

### Presenting the data

<!--
Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

- [ ] Provide visual examples on how the dashboard looks. Pictures needed.
- [ ] How often is data saved in the database.
- [ ] \*Explain your choice of database.
- [ ] \*Automation/triggers of the data.
-->

### Finalizing the design

<!--
Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

- [ ] Show final results of the project
- [ ] Pictures
- [ ] \*Video presentation
-->

---

## Useful links:
- [DHT11 sensor example for RP2](https://github.com/iot-lnu/applied-iot/tree/master/Raspberry%20Pi%20Pico%20(W)%20Micropython/sensor-examples/P5_DHT_11_DHT_22)
- [FC-28 sensor example for Arduino](https://lastminuteengineers.com/soil-moisture-sensor-arduino-tutorial/)
- [Measuring from the analog pins on RP2](https://pycopy.readthedocs.io/en/latest/rp2/quickref.html#adc-analog-to-digital-conversion)
