from time import sleep

from PIL import Image
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text


class EyeLedMatrix(max7219):
    def preprocess(self, image):
        image = super(EyeLedMatrix, self).preprocess(image)
        upper = image.crop((0, 0, image.width, image.height/2))  # TODO: get upper half
        upper = upper.transpose(Image.FLIP_TOP_BOTTOM)
        upper = upper.transpose(Image.FLIP_LEFT_RIGHT)
        image.paste(upper)
        return image


class LedMatrices:
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = EyeLedMatrix(serial, width=16, height=16)

    def __draw(self, drawing_function):
        with canvas(self.device) as draw:
            drawing_function(draw)

    def __eye_debug_drawer(self, draw):
        draw.rectangle(self.device.bounding_box, outline="white", fill="black")
        text(draw, (2, 2), 'Pino', fill='white')

    def __eye_neutral_drawer(self, draw):
        draw.arc(self.device.bounding_box, 0, 360, fill='white')
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
        self.device.clear()
        self.device.cleanup()

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


