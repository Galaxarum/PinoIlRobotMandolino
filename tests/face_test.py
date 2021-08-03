from ..led_matrices import LedMatrices
from time import sleep

matrix = LedMatrices()

matrix.eye_neutral()
sleep(2)
matrix.eye_angry()
sleep(2)
matrix.eye_sad()
sleep(2)
matrix.eye_x()
sleep(2)
matrix.eye_flat()
sleep(2)
matrix.eye_bored()
