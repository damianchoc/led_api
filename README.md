<h1> FLASK APP to controll your WS2811 led strip and power(relay)</h1>

App runs api that let you controll your let strip via http requests:

(your IP):4040/changeColor/(String color) - expect color name from 'colors' collection from <b>led.py</b>. You can add own if you want to<br/>
(your IP):4040/brightness/(int percent) - it doesn't work yet<br/>
(your IP):4040/switchOn - switch on led strip by relay<br/>
(your IP):4040/switchOff - switch off led strip by relay<br/>
(your IP):4040/status - gives status if led is turned on or off. Gives '1' or '0'<br/>
(your IP):4040/htmlColor/(string color) - expect html code color '#XXXXXX' or 'XXXXXX'<br/>

<h2>Config:</h2>

LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).<br/>
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)<br/>
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)<br/>
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest<br/>
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)<br/>
LED_POWER_SWITCH = 2    # relay pin for turn on/off led strip<br/>
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53<br/>

code based on https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
