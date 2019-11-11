from flask_restful import Resource
from flask.views import MethodView
import json
import time
from neopixel import *
import RPi.GPIO as GPIO
import logging

# LED CONFIG
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_POWER_SWITCH = 2    # relay pin for turn on/off led strip
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# LOG CONFIG
logger = logging.getLogger('led_api')
logger.setLevel(logging.DEBUG)
# specify where you want log file
fh = logging.FileHandler('/var/log/led_api.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_POWER_SWITCH, GPIO.OUT)

def html_color_to_rgb(colorstring):
    # convert #RRGGBB to Color(b,r,g) object
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        logger.error('Given invalid color html code, given code: %s', colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return Color(b, r, g)

def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theater_chase(strip, color, wait_ms=50, iterations=10):
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

def rainbow_cycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theater_chaseRainbow(strip, wait_ms=50):
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

# meh, works BRG instead of RGB, don't know why
colors = {
"red" : Color(0, 255, 0),
"blue" : Color(255, 0, 0),
"green" : Color(0, 0, 255),
"DaronGreen" : Color(15,24,216),
"DaronGreenLight" : Color(37,46,248),
"MayaBlue" : Color(243,26,195),
"MayaBlueLight" : Color(251,88,250),
"NightBlue" : (180,0,0),
"Lime" : Color(106,255,172),
"Moonlight" : Color(136,199,201),
"WhiteTheater" : Color(127, 127, 127)
}

powerStatus = 0
settedColor = 'unknown'

class change_color(Resource):
    def get(self, color):
        global settedColor
        logger.info('Changing color to %s', color)
        if color in colors.keys():
            colorWipe(strip, colors[color])
            settedColor = color
            return {'OK, Setting color:' : color}
        elif color == "rainbow":
            rainbow(strip)
            settedColor = color
        elif color == "rainbowCycle":
            rainbowCycle(strip)
            settedColor = color
        else:
            return {'dont known color: ' : color}

class html_color(Resource):
    def get(self, color):
        global settedColor
        logger.info('Changing color to %s', color)
        colorWipe(strip, HTMLColorToRGB(color))
        settedColor = color
        return {'OK, Setting color: ' : color}


# brightness todo
class brightness(Resource):
    def get(self, percent):
        return {'some':'bright'}

class switch_on(Resource):
    def get(self):
        global powerStatus
        logger.info('Switchin on')
        GPIO.output(LED_POWER_SWITCH, GPIO.HIGH)
        powerStatus = 1
        if settedColor != 'unknown':
            logger.info('Seems color is set up. Setting')
            try:
                colorWipe(strip, HTMLColorToRGB(settedColor))
                logger.info('Preious color set succesfully')
            except Exception as e:
                logger.error('Error witch setting previous color')
        return {'switch':"on"}

class switch_off(Resource):
    def get(self):
        global powerStatus
        logger.info('Switchin off')
        GPIO.output(LED_POWER_SWITCH, GPIO.LOW)
        powerStatus = 0
        return {'switch':"off"}

class status(Resource):
    def get(self):
        global powerStatus
        return powerStatus

class get_color(Resource):
    def get(self):
        global settedColor
        return settedColor
