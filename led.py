from flask_restful import Resource
from flask.views import MethodView
import json

# LED CONFIG
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#for testing
class Color():
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
#/

colors = {
"red" : Color(255, 0, 0),
"blue" : "blue",
"green" : "green",
"white" : "white"
}

class ChangeColor(Resource):
    def get(self, color):
        return {'color': colors[color]}

class Brightness(Resource):
    def get(self):
        return {'some':'bright'}

class SwitchOn(Resource):
    def get(self):
        return {'switch':"on"}

class SwitchOff(Resource):
    def get(self):
        return {'switch':"off"}

class Status(Resource):
    def get(self):
        return {'show':"status"}
