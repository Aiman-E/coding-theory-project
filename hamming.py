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

    # calculate the syndrome to check if the received block has an error in it
    def syndrome(self, received_block):
        received_block = np.array(received_block, dtype=np.uint8)
        H_transpose = np.transpose(self.H)
        syndrome_value = np.matmul(received_block, H_transpose)
        syndrome_value = np.mod(syndrome_value, 2)

        return syndrome_value


    # take the message block and dencode it and check for corruption
    def decode_block(self, received_block):
        received_block = np.array(received_block, dtype=np.uint8)
        syndrome_value = self.syndrome(received_block)
        corrected_block = received_block.copy()

        if not np.all(syndrome_value == 0):
            error_position = -1
            for column_index in range(self.n):
                H_column = self.H[:, column_index]
                if np.array_equal(H_column, syndrome_value):
                    error_position = column_index
                    break

            if error_position != -1:
                corrected_block[error_position] = np.mod(
                    corrected_block[error_position] + 1,
                    2
                )

        message_block = corrected_block[:self.k]
        return message_block

    # split the message into blocks then dencode them
    def decode(self, bits):
        bits = np.array(bits, dtype=np.uint8)
        received_blocks = bits.reshape(-1, self.n)

        decoded_blocks = []

        for block in received_blocks:
            decoded_block = self.decode_block(block)
            decoded_blocks.append(decoded_block)

        decoded_bits = np.array(decoded_blocks, dtype=np.uint8)
        decoded_bits = decoded_bits.reshape(-1)

        return decoded_bits

    def build_g_matrix(self, H_matrix):
        H_matrix = np.array(H_matrix, dtype=np.uint8)

        P_transpose = H_matrix[:, : self.k]
        P = P_transpose.T
        I = np.eye(self.k, dtype=np.uint8)

        G = np.concatenate((I, P), axis=1)

        return G
