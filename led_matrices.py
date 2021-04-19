from time import sleep

from PIL import Image
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.virtual import viewport
from luma.core.legacy import text
from threading import Thread
import math
import atexit


class EyeLedMatrix(max7219):
    def preprocess(self, image):
        image = super(EyeLedMatrix, self).preprocess(image)
        upper = image.crop((0, 0, image.width, image.height/2))
        upper = upper.transpose(Image.FLIP_TOP_BOTTOM)
        upper = upper.transpose(Image.FLIP_LEFT_RIGHT)
        image.paste(upper)
        return image


def _plot_sin(draw, size, amplitude=None, steps=None):
    if amplitude is None:
        amplitude = size[1]/2-1
    if steps is None:
        steps = min(size)
    prev = (0, size[1]/2)
    for r in range(int(size[0] / steps)):
        for i in range(steps):
            x = 2 * math.pi * (i / steps)
            y = amplitude * math.sin(x)
            y = int(y)
            y += size[1] / 2
            point = (i + r * steps, y)
            draw.point(point, fill='white')
            draw.line([prev, point])
            prev = point


class LedMatrices:
    def __init__(self):
        serial0 = spi(port=0, device=0, gpio=noop())
        self.eyes = EyeLedMatrix(serial0, width=16, height=16)

        serial1 = spi(port=1, device=0, gpio=noop())
        self.mouth_matrix = max7219(serial1)
        self.mouth = viewport(self.mouth_matrix, width=32, height=16)

        def scroll_mouth():
            while self.mouth is not None:
                for offset in range(self.mouth.width):
                    self.mouth.set_position((offset, 0))
                    sleep(0.1)
        Thread(target=scroll_mouth).start()

        self.eye_neutral()
        self.stop_speak()

        atexit.register(self.clear)

    def clear(self):
        self.mouth.clear()
        self.mouth = None
        self.mouth_matrix.clear()
        self.eyes.clear()

    def speak(self):
        with canvas(self.mouth) as draw:
            _plot_sin(draw, size=self.mouth.size)

    def stop_speak(self):
        with canvas(self.mouth) as draw:
            _plot_sin(draw, size=self.mouth.size, amplitude=2)

    def __draw(self, drawing_function):
        with canvas(self.eyes) as draw:
            drawing_function(draw)

    def __eye_debug_drawer(self, draw):
        draw.rectangle(self.eyes.bounding_box, outline="white", fill="black")
        text(draw, (2, 2), 'Pino', fill='white')

    def __eye_neutral_drawer(self, draw):
        draw.arc(self.eyes.bounding_box, 0, 360, fill='white')
        draw.ellipse([(6, 6), (9, 9)], outline='white', fill='white')

    def __eye_angry_drawer(self, draw, angle):
        self.__eye_neutral_drawer(draw)
        draw.pieslice([(0, 0), (15, 15)], 180+angle, -angle, fill='white')

    def __eye_flat_drawer(self, draw, angle):
        self.__eye_neutral_drawer(draw)
        draw.chord([(0, 0), (15, 15)], 180 + angle, -angle, outline='white', fill='white')

    def __eye_sad_drawer(self, draw, angle):
        self.__eye_neutral_drawer(draw)
        draw.chord([(0, 0), (15, 15)], 180, -angle, fill='white')
        draw.chord([(0, 0), (15, 15)], 180 + angle, 360, fill='white')

    def eye_debug(self):
        self.__draw(self.__eye_debug_drawer)
        sleep(1)
        self.eye_neutral()
        sleep(1)
        self.eye_suspicious()
        sleep(1)
        self.eye_bored()
        sleep(1)
        self.eye_sad()
        sleep(1)
        self.eye_angry()
        sleep(1)
        self.eyes.clear()

    def eye_neutral(self):
        self.__draw(self.__eye_neutral_drawer)

    def eye_angry(self, angle=20):
        self.__draw(lambda draw: self.__eye_angry_drawer(draw, angle=angle))

    def eye_suspicious(self, angle=25):
        self.__draw(lambda draw: self.__eye_flat_drawer(draw, angle=angle))

    def eye_bored(self, angle=10):
        self.__draw(lambda draw: self.__eye_flat_drawer(draw, angle=angle))

    def eye_sad(self, angle=45):
        self.__draw(lambda draw: self.__eye_sad_drawer(draw, angle=angle))
