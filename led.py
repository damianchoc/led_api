from flask_restful import Resource
from flask.views import MethodView
import json
import time
from neopixel import *
import argparse
import RPi.GPIO as GPIO

# LED CONFIG
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_POWER_SWITCH = 2    # relay pin for turn on/off led strip
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_POWER_SWITCH, GPIO.OUT)


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

colors = {
"red" : Color(0, 255, 0),
"blue" : Color(255, 0, 0),
"green" : Color(0, 0, 255),
"DaronGreen" : Color(15,216,024),
"DaronGreenLight" : Color(37,248,46),
"MayaBlue" : Color(26,195,243),
"MayaBlueLight" : Color(88,250,251),
"Night Blue" : (0,0,180),
"Lime" : Color(172,255,106),
"Moonlight" : Color(201,199,136),
"White theater" : Color(127, 127, 127),
"white" : "white",
"rainbow" : "rainbow",
"rainbowCykle" : "rainbowCycle"
}

powerStatus = 'off'
settedColor = 'unknown'

class ChangeColor(Resource):
    def get(self, color):
        if color in colors.keys():
            colorWipe(strip, colors[color])
            settedColor = color;
            return {'OK, Setting color:' : color}
        elif color == "rainbow":
            rainbow(strip)
            settedColor = color
        elif color == "rainbowCycle":
            rainbowCycle(strip)
            settedColor = color
        else:
            return {'dont known color: ' : color}

# brightness todo
class Brightness(Resource):
    def get(self, percent):
        return {'some':'bright'}

class SwitchOn(Resource):
    def get(self):
        GPIO.output(LED_POWER_SWITCH, GPIO.HIGH)
        powerStatus = 'on'
        return {'switch':"on"}

class SwitchOff(Resource):
    def get(self):
        GPIO.output(LED_POWER_SWITCH, GPIO.LOW)
        powerStatus = 'off'
        return {'switch':"off"}

class Status(Resource):
    def get(self):
        return {'Led power':powerStatus, 'color':settedColor}
