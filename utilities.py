# This file will have helper functions to be used in the project

import numpy as np


def text_to_bits(text):
    bits = []

    for character in text:
        ascii_value = ord(character)
        binary_string = format(ascii_value, "08b")

        for bit in binary_string:
            bits.append(int(bit))

    return np.array(bits, dtype=np.uint8)
