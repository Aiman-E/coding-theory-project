# Hamming code class definition
from utilities import *
import numpy as np


class HammingCode:
    def __init__(self, H, k):
        self.H = H  # H is the parity-check matrix from parameters
        self.k = k  # k is the number of original message bits in one block

        self.n = self.H.shape[
            1
        ]  # take the n(number of bits in one block) from the number of columns in H

        self.G = self.build_g_matrix(self.H)  # store the generator matrix

    # take the message block and encode it
    def encode_block(self, message_block):
        message_block = np.array(message_block, dtype=np.uint8)
        codeword = np.matmul(message_block, self.G)
        codeword = np.mod(codeword, 2)
        return codeword

    # split the message into blocks then encode them
    def encode(self, bits):
        bits = np.array(bits, dtype=np.uint8)

        # convert the bits into blocks with size of k
        message_blocks = bits.reshape(-1, self.k)
        encoded_blocks = []

        # encode blocks
        for block in message_blocks:
            encoded_block = self.encode_block(block)  # encode block
            encoded_blocks.append(encoded_block)

        encoded_bits = np.array(encoded_blocks, dtype=np.uint8)
        # remove the block structure and make it one full array of bits
        encoded_bits = encoded_bits.reshape(-1)

        return encoded_bits

    # calculate the syndrome to check if the received block has an error in it
    def syndrome(self, received_block):
        received_block = np.array(received_block, dtype=np.uint8)
        H_transpose = np.transpose(
            self.H
        )  # in order to multiply H with the received block we need to get H_transpose
        syndrome_value = np.matmul(received_block, H_transpose)
        syndrome_value = np.mod(
            syndrome_value, 2
        )  # get mod 2 of syndrome to get it in binary
        return syndrome_value

    # take the message block and dencode it and check for corruption
    def decode_block(self, received_block):
        received_block = np.array(received_block, dtype=np.uint8)
        syndrome_value = self.syndrome(received_block)
        corrected_block = (
            received_block.copy()
        )  # make a copy so we can correct it without changing the origin

        # if syndrome is not full non-zero, there is an error we need to fix
        if not np.all(syndrome_value == 0):
            error_position = -1  # reset the error position, -1 means no error detected

            # Check every column in H
            for column_index in range(self.n):
                H_column = self.H[:, column_index]  # get current column

                # if the column equal the syndrome calculated then it is the column with the error
                if np.array_equal(H_column, syndrome_value):
                    error_position = column_index
                    break

            # if there is an error, flip it
            if error_position != -1:
                corrected_block[error_position] = np.mod(
                    corrected_block[error_position] + 1, 2
                )

        message_block = corrected_block[: self.k]
        # take the first k bits without the added bits that where added in the encoding
        return message_block

    # split the message into blocks then dencode them
    def decode(self, bits):
        bits = np.array(bits, dtype=np.uint8)
        received_blocks = bits.reshape(
            -1, self.n
        )  # change the list of bits into blocks of size n
        decoded_blocks = []

        # Decode each received block one by one and store them
        for block in received_blocks:
            decoded_block = self.decode_block(block)
            decoded_blocks.append(decoded_block)

        decoded_bits = np.array(decoded_blocks, dtype=np.uint8)
        decoded_bits = decoded_bits.reshape(-1)  # make it one bit array of bits

        return decoded_bits

    def build_g_matrix(self, H_matrix):
        H_matrix = np.array(H_matrix, dtype=np.uint8)

        P_transpose = H_matrix[:, : self.k]  # take first k columns from H_matrix
        P = P_transpose.T  # get P
        I = np.eye(self.k, dtype=np.uint8)

        G = np.concatenate(
            (I, P), axis=1
        )  # join I and P horizontally not vertically to get the g matrix

        return G

    # As the project sheet requires, add a check for the generator matrix
    def check_the_generator_matrix(self):
        print("Generator matrix check:")
        print("  G shape:", self.G.shape)
        print("  H shape:", self.H.shape)

        G_times_H_transpose = np.matmul(self.G, np.transpose(self.H))
        check = np.mod(G_times_H_transpose, 2)

        print("  G mult H.T mod 2:")
        print(check)
        print("  Passed:", np.all(check == 0))
        print()
