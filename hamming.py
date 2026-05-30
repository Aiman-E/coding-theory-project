# Hamming code class definition
from utilities import *
import numpy as np


class HammingCode:
    def __init__(self, H, k):
        self.H = H
        self.k = k
        self.n = self.H.shape[1]
        self.G = self.build_g_matrix(self.H)

    # take the message block and encode it
    def encode_block(self, message_block):
        message_block = np.array(message_block, dtype=np.uint8)
        codeword = np.matmul(message_block, self.G)
        codeword = np.mod(codeword, 2)
        return codeword

    # split the message into blocks then encode them
    def encode(self, bits):
        bits = np.array(bits, dtype=np.uint8)
        message_blocks = bits.reshape(-1, self.k)
        encoded_blocks = []

        for block in message_blocks:
            encoded_block = self.encode_block(block)
            encoded_blocks.append(encoded_block)

        encoded_bits = np.array(encoded_blocks, dtype=np.uint8)
        encoded_bits = encoded_bits.reshape(-1)

        return encoded_bits

    def syndrome(self):
        pass

    def decode_block(self):
        pass

    def decode(self):
        pass

    def build_g_matrix(self, H_matrix):
        H_matrix = np.array(H_matrix, dtype=np.uint8)

        P_transpose = H_matrix[:, : self.k]
        P = P_transpose.T
        I = np.eye(self.k, dtype=np.uint8)

        G = np.concatenate((I, P), axis=1)

        return G
