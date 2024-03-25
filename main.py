# ! still need to add the libraries to version control

import time
import board
import adafruit_hcsr04
import digitalio
import simpleio
from neopixel import NeoPixel

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
led = digitalio.DigitalInOut(board.D11)
led.direction = digitalio.Direction.OUTPUT
onboardLed = NeoPixel(board.NEOPIXEL, 1, brightness=1.0, auto_write=True)

# * The LED on the feather board is not actually needed for the baby alarm. The battery pack we're using
# * goes to sleep after a while if a certain amount of current isn't being drawn, and the rest of the baby
# * alarm circuit isn't enough. So to simulate a heavier load, we're turning the onboard LED all of the way 
# * on and up. If we switch out for a different board like a trinket we may need to figure out a different
# * way of simulating a heavier load. 
onboardLed[0] = (255,255,255)

trigger = 70
note_frequencies = { 'C6': 1047, 'D6': 1175, 'E6': 1319, 'F6': 1397, 'G6': 1568, 'A6': 1760, 'B6': 1976, 'C7': 2093, 'D7': 2349, 'E7': 2637, 'F7': 2794, 'G7': 3136, 'A7': 3520, 'B7': 3951, 'C8': 4186, 'D8': 4698, 'E8': 5274, 'F8': 5588, 'G8': 6272, 'A8': 7040, 'B8': 7902 }

while True:
    try:
      if sonar.distance < trigger:
        print("===> BABY ALERT <===")
        led.value = True
        for f in ([note_frequencies['C7'], note_frequencies['F7']]):
            simpleio.tone(board.A2, f, 0.15)

      else:
        led.value = False
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)
