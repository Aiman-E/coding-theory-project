# This file will define the project experiments required by the prof
import parameters as params
import hamming
import convolutional
from utilities import *
import time


def hamming_only():
    print("=" * 50)
    print("HAMMING CODE TEST")
    print("=" * 50)

    hamming_encoder = hamming.HammingCode(params.H, params.k)

    message_bits = text_to_bits(params.personal_message)
    encoded_bits = hamming_encoder.encode(message_bits)
    decoded_bits = hamming_encoder.decode(encoded_bits)

    expected_length = int(len(message_bits) / hamming_encoder.k * hamming_encoder.n)

    print("Original message:")
    print(" ", params.personal_message)
    print()

    print("Hamming parameters:")
    print("  k =", hamming_encoder.k, "message bits per block")
    print("  n =", hamming_encoder.n, "encoded bits per block")
    print()

    print_bits_summary("Original message bits:", message_bits)
    print_bits_summary("Encoded bits:", encoded_bits)

    print("Encoding test:")
    print("  Expected encoded length:", expected_length)
    print("  Actual encoded length:  ", len(encoded_bits))
    print("  Passed:", len(encoded_bits) == expected_length)
    print()

    print_bits_summary("Decoded bits:", decoded_bits)

    print("Decoding test:")
    print("  Passed:", np.array_equal(message_bits, decoded_bits))
    print()

    print("-" * 50)
    print("SINGLE-BIT ERROR CORRECTION TEST")
    print("-" * 50)

    corrupted_bits = encoded_bits.copy()

    error_position = 2
    corrupted_bits[error_position] = np.mod(corrupted_bits[error_position] + 1, 2)

    decoded_corrupted_bits = hamming_encoder.decode(corrupted_bits)

    print("Corruption:")
    print("  Flipped bit position:", error_position)
    print("  Original bit:", encoded_bits[error_position])
    print("  Corrupted bit:", corrupted_bits[error_position])
    print()

    print_bits_summary("Corrupted encoded bits:", corrupted_bits)
    print_bits_summary("Decoded corrupted bits:", decoded_corrupted_bits)

    print("Single-bit error correction test:")
    print("  Passed:", np.array_equal(message_bits, decoded_corrupted_bits))
    print()

    print("=" * 50)


def convolutional_only():
    print("=" * 50)
    print("CONVOLUTIONAL CODE TEST")
    print("=" * 50)

    convolutional_encoder = convolutional.Convolutional(
        params.generators, params.K, params.memory
    )

    message_bits = text_to_bits(params.personal_message)

    encoded_bits_terminated = convolutional_encoder.encode(message_bits, terminate=True)
    encoded_bits_not_terminated = convolutional_encoder.encode(
        message_bits, terminate=False
    )

    number_of_generators = len(convolutional_encoder.generators)

    expected_length_not_terminated = len(message_bits) * number_of_generators

    expected_length_terminated = (
        len(message_bits) + convolutional_encoder.memory
    ) * number_of_generators

    print("Original message:")
    print(" ", params.personal_message)
    print()

    print("Convolutional parameters:")
    print("  Constraint length:", convolutional_encoder.constraint_length)
    print("  Memory:", convolutional_encoder.memory)
    print("  Number of states:", convolutional_encoder.num_states)
    print("  Number of generators:", number_of_generators)
    print("  Generators:")
    print(convolutional_encoder.generators)
    print()

    print_bits_summary("Original message bits:", message_bits)

    print_bits_summary("Encoded bits without termination:", encoded_bits_not_terminated)
    print_bits_summary("Encoded bits with termination:", encoded_bits_terminated)

    print("Encoding length test without termination:")
    print("  Expected encoded length:", expected_length_not_terminated)
    print("  Actual encoded length:  ", len(encoded_bits_not_terminated))
    print(
        "  Passed:", len(encoded_bits_not_terminated) == expected_length_not_terminated
    )
    print()

    print("Encoding length test with termination:")
    print("  Expected encoded length:", expected_length_terminated)
    print("  Actual encoded length:  ", len(encoded_bits_terminated))
    print("  Passed:", len(encoded_bits_terminated) == expected_length_terminated)
    print()

    print("-" * 50)
    print("STATE TRANSITION TEST")
    print("-" * 50)

    state = 0

    print("Start state:", state)
    print("Start state bits:", convolutional_encoder.state_to_bits(state))
    print()

    for bit in message_bits[:8]:
        output = convolutional_encoder.output_bits(bit, state)
        next_state = convolutional_encoder.next_state(bit, state)

        print("Input bit:", bit)
        print("  Current state:", state)
        print("  Current state bits:", convolutional_encoder.state_to_bits(state))
        print("  Output bits:", output)
        print("  Next state:", next_state)
        print("  Next state bits:", convolutional_encoder.state_to_bits(next_state))
        print()

        state = next_state

    print("=" * 50)
