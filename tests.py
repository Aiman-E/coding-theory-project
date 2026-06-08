# This file will include tests for single class functionality for debugging


# test encoder based on pre-defined example
def state_transition_table(encoder):
    print("-" * 50)
    print("FULL STATE TRANSITION TABLE")
    print("-" * 50)

    for state in range(encoder.num_states):
        for input_bit in [0, 1]:
            output = encoder.output_bits(input_bit, state)
            next_state = encoder.next_state(input_bit, state)

            print(
                "State",
                state,
                encoder.state_to_bits(state),
                "+ input",
                input_bit,
                "-> output",
                output,
                "next state",
                next_state,
                encoder.state_to_bits(next_state),
            )
