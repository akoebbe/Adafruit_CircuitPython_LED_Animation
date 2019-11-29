# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_led_animation.animation`
================================================================================

CircuitPython helper library for LED animations.


* Author(s): Roy Hooper, Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import time
import random
from .color import BLACK

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"


class Animation:
    # TODO: rename pixel_object to something more beginner friendly
    def __init__(self, pixel_object, speed, color):
        self.pixel_object = pixel_object
        self.speed = speed
        self._color = color
        self._next_update = time.monotonic()
        self.pixel_object.auto_write = False
        self.color = color

    def animate(self):
        """
        Call animate() from your code's main loop.  It will draw the animation draw() at intervals configured by
        The speed property (set from init).
        :return: True if the animation draw cycle was triggered, otherwise False.
        """
        now = time.monotonic()
        if now < self._next_update:
            return False

        self._next_update = now + self.speed
        self.draw()
        return True

    def draw(self):
        """
        Animation subclasses must implement draw() to render the animation sequence.
        """
        pass

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, int):
            value = (value >> 16 & 0xff, value >> 16 & 0xff, value & 0xff)
        self._color = value
        self._recompute_color(value)

    def _recompute_color(self, color):
        pass


class Blink(Animation):
    def __init__(self, pixel_object, speed, color, color_off=BLACK):
        self.color_off = color_off
        self._state = False
        super(Blink, self).__init__(pixel_object, speed, color)

    def draw(self):
        self._state = not self._state
        self.pixel_object.fill(self.color if self._state else self.color_off)
        self.pixel_object.show()


class Comet(Animation):
    def __init__(self, pixel_object, speed, color, tail_length=10):
        self._tail_length = tail_length
        self._color_step = 0.8 / tail_length
        self._color_offset = 0.2
        self._comet_colors = None
        super(Comet, self).__init__(pixel_object, speed, color)
        self._generator = self._comet_generator()

    def _recompute_color(self, color):
        self._comet_colors = [
            [int(color[rgb] * ((n * self._color_step) + self._color_offset))
             for rgb in range(len(color))
            ] for n in range(self._tail_length)
        ]

    def _comet_generator(self):
        num_pixels = len(self.pixel_object)
        while True:
            for start in range(-self._tail_length, num_pixels + 1):
                if start > 0:
                    self.pixel_object[start-1] = 0
                if start + self._tail_length < num_pixels:
                    end = self._tail_length
                else:
                    end = num_pixels - start
                if start < 0:
                    num_visible = self._tail_length + start
                    self.pixel_object[0:num_visible] = self._comet_colors[self._tail_length -
                                                                          num_visible:]
                else:
                    self.pixel_object[start:start + end] = self._comet_colors[0:end]
                self.pixel_object.show()
                yield

    def draw(self):
        next(self._generator)


class Sparkle(Animation):
    def __init__(self, pixel_object, speed, color):
        self._half_color = None
        self._dim_color = None
        super(Sparkle, self).__init__(pixel_object, speed, color)

    def _recompute_color(self, color):
        half_color = tuple(color[rgb] // 2 for rgb in range(len(color)))
        dim_color = tuple(color[rgb] // 10 for rgb in range(len(color)))
        for pixel in range(len(self.pixel_object)):
            if self.pixel_object[pixel] == self._half_color:
                self.pixel_object[pixel] = half_color
            else:
                self.pixel_object[pixel] = dim_color
        self._half_color = half_color
        self._dim_color = dim_color

    def draw(self):
        pixel = random.randint(0, (len(self.pixel_object) - 2))
        self.pixel_object[pixel] = self._color
        self.pixel_object.show()
        self.pixel_object[pixel] = self._half_color
        self.pixel_object[pixel + 1] = self._dim_color
        self.pixel_object.show()
