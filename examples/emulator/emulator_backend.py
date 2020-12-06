from neopixel_emulator import NeoPixel_Emulator
import neopixel


class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = "adafruit_blinka"

    def __init__(self, id):
        self.id = id

    def init(self, mode=0, pull=None):
        pass

    def value(self, val=None):
        return 1


class Adafruit_NeoPixel_Emulator(neopixel.NeoPixel):
    def __init__(
            self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None
    ):
        super().__init__(
            pin, n, bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=None
        )

    def deinit(self):
        """Blank out the NeoPixels and release the pin."""
        self.fill(0)
        self.show()

    def begin(self, draw_matrix=False, width=0, height=0, window_w=1765, window_h=400):
        self.gui = NeoPixel_Emulator(window_w=window_w, window_h=window_h)
        if draw_matrix:
            self.gui.draw_LED_matrix(width, height)
        else:
            self.gui.draw_LEDs(self._pixels)
        self.gui.render()

    def _transmit(self, buffer):
        for pixel_position in range(0, self._pixels):
            self.gui.draw_color(pixel_position, self._getitem(pixel_position))
        self.gui.render()

