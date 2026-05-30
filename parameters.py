# This file contains the parameters set i will be using throughout this project
import numpy as np

# hamming parameters

n = 7  # codeword length
k = 4  # message bit length

H = np.array(
    [[1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1]],
)  # parity-check matrix


# Convolutional parameters
K = 4
memory = 3
states = 8

g1 = [1, 1, 0, 1]

g2 = [1, 0, 1, 1]

# experiment settings

personal_message = "ECC2026-S04D"

seeds = [6453, 11757, 19257]

ber_values = [0.001, 0.01, 0.05, 0.10, 0.15]
