from .K4_N8_6x6 import K4_N8_6x6
from .K6_N8_3x3 import K6_N8_3x3
from .K6_N8_12x12_BD import K6_N8_12x12_BD
from .K6_N8_28x28_BD import K6_N8_28x28_BD


def setup():
    return [
        K4_N8_6x6.setup(),
        K6_N8_3x3.setup(),
        K6_N8_12x12_BD.setup(),
        K6_N8_28x28_BD.setup()
    ]
