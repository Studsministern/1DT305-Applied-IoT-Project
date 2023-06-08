from machine import Pin
import utime as time

# Set the led pin
led_onboard = Pin("LED", Pin.OUT)

while True:
    led_onboard.toggle()
    ''' Alternative to toggle() is either changing the value() or using on() & off() methods '''
    time.sleep(.5)       # Delay for 1 second