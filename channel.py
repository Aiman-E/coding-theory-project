# This file will handle binary symmetrical channel
import numpy as np


def Binary_Symmetric_Channel(bits, ber, seed):
    rng = np.random.default_rng(seed)
    bits = np.array(bits, dtype=np.uint8)

    flip_mask = rng.random(bits.size) < ber
    received = bits.copy()

    received[flip_mask] ^= 1
    errors_before = int(flip_mask.sum())

    return received, errors_before
