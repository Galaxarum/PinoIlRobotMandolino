from PIL import Image
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219


class EyeLedMatrix(max7219):
    def preprocess(self, image):
        super(EyeLedMatrix, self).preprocess(image)
        upper = image.crop((0, 0, image.width-1, image.height/2-1))  # TODO: get upper half
        upper = upper.transpose(Image.FLIP_TOP_BOTTOM)
        image.paste(upper)
        return image


serial = spi(port=0, device=0, gpio=noop())
device = EyeLedMatrix(serial, width=16, height=16)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
