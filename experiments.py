# This file will define the project experiments required by the prof
import parameters as params
import hamming
from utilities import *


def hamming_only():
    hamming_encoder = hamming.HammingCode(params.H, params.k)
    message_bits = text_to_bits(params.personal_message)
    encoded_bits = hamming_encoder.encode(message_bits)

    print("Original message:", params.personal_message)
    print("Original bit length:", len(message_bits))
    print("Encoded bit length:", len(encoded_bits))
    print("Encoded bits:", encoded_bits)

    expected_length = int(len(message_bits) / hamming_encoder.k * hamming_encoder.n)

    print("Expected encoded length:", expected_length)
    print("Encoding test passed:", len(encoded_bits) == expected_length)
