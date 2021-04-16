from luma.core.interface.serial import spi, noop
from luma.core.legacy import text
from luma.core.render import canvas
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=16, height=16)

with canvas(device) as draw:
    text(draw, (0, 0), 'Hello', fill='white')
