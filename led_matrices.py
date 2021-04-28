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
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        upper = image.crop((0, 0, image.width, image.height/2))
        upper = upper.transpose(Image.FLIP_TOP_BOTTOM)
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
            draw.line([prev, point], fill='white', width=1)
            prev = point


class LedMatrices:
    def __init__(self):
        serial0 = spi(port=0, device=0, gpio=noop())
        self.eyes = EyeLedMatrix(serial0, width=16, height=16)
        serial1 = spi(port=1, device=0, gpio=noop())
        self.mouth_matrix = max7219(serial1, cascaded=2)
        self.mouth = viewport(self.mouth_matrix, width=24, height=8)
        self.enabled = True

        def scroll_mouth():
            while self.enabled:
                for offset in range(self.mouth.width // 3):
                    self.mouth.set_position((offset, 0))

                    sleep(0.05)
        Thread(target=scroll_mouth, name='Mouth scroller').start()

        self.eye_neutral()
        self.stop_speak()

        atexit.register(lambda: self.clear())

    def clear(self):
        self.enabled = False
        self.mouth.clear()
        self.mouth_matrix.clear()
        self.eyes.clear()
        
    def speak(self):
        with canvas(self.mouth) as draw:
            _plot_sin(draw, size=self.mouth.size)

    def stop_speak(self):
        with canvas(self.mouth) as draw:
            _plot_sin(draw, size=self.mouth.size, amplitude=2, steps=2)

    def __draw(self, drawing_function):
        with canvas(self.eyes) as draw:
            drawing_function(draw)

    def __eye_neutral_drawer(self, draw):
        draw.arc(self.eyes.bounding_box, 0, 360, fill='white')
        draw.ellipse([(6, 6), (9, 9)], outline='white', fill='white')

    def eye_debug(self):
        with canvas(self.eyes) as draw:
            draw.rectangle(self.eyes.bounding_box, outline="white", fill="black")
            text(draw, (2, 2), 'Pino', fill='white')
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
        self.eye_x()
        sleep(1)
        self.eyes.clear()

    def eye_neutral(self):
        with canvas(self.eyes) as draw:
            self.__eye_neutral_drawer(draw)

    def eye_angry(self, angle=30):
        with canvas(self.eyes) as draw:
            self.__eye_neutral_drawer(draw)
            draw.pieslice([(3, 0), (12, 10)], 180 + angle, -angle, fill='white')

    def eye_flat(self, angle=17):
        with canvas(self.eyes) as draw:
            self.__eye_neutral_drawer(draw)
            draw.chord([(0, 0), (15, 15)], 180 + angle, -angle, outline='white', fill='white')

    def eye_suspicious(self):
        self.eye_flat(angle=25)

    def eye_bored(self):
        self.eye_flat(angle=10)

    def eye_sad(self, angle=45):
        with canvas(self.eyes) as draw:
            self.__eye_neutral_drawer(draw)
            draw.chord([(0, 0), (15, 15)], 180, -angle, fill='white')
            draw.chord([(0, 0), (15, 15)], 180 + angle, 360, fill='white')

    def eye_x(self):
        with canvas(self.eyes) as draw:
            draw.line([(0, 0), (15, 15)], fill='white')
            draw.line([(15, 0), (0, 15)], fill='white')
