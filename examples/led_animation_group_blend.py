from emulator.emulator_backend import Adafruit_NeoPixel_Emulator, Pin

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.group import AnimationGroup
import adafruit_led_animation.color as color


def run():
    pixels = Adafruit_NeoPixel_Emulator(Pin(3), n=30, auto_write=True)
    pixels.begin()
    pixels.fill(0)

    comet1 = Comet(pixels, 0.2, color.RED, 6, bounce=True)
    comet2 = Comet(pixels, 0.4, color.WHITE, 6, bounce=True)
    comet3 = Comet(pixels, 0.7, color.GREEN, 6, bounce=True)

    group = AnimationGroup(comet1, comet2, comet3, sync=False)

    while True:
        group.animate()

    # pixels.setBrightness(100)
    # pixels.setPixelColor(2,pixels.Color(255,200,10))
    # pixels.show()
    # pixels.delay(200)
    # pixels.fill(pixels.Color(150,60,10),4,10)
    # pixels.show()
    # pixels.delay(1000)
    # pixels.clear()
    # effects.colorWipe(pixels.Color(200,12,70),50)
    # pixels.setBrightness(70)
    # pixels.clear()
    # pixels.show()
    # pixels.delay(1000)
    # for i in range(5):
    #     effects.colorWipe(pixels.Color(200,0,200),10)
    #     pixels.clear()
    # pixels.setBrightness(90)
    # effects.rainbow(20)
    # effects.colorWipe(pixels.Color(150,150,0),40)
    # effects.rainbowCycle(20,2)


run()
