import parameters as params
from parameters import *
import numpy as np

"""
# obtain the Generator matrix from the H matrix .

 we need 2 main functions, a modulus-2 function and a function that do encoding c=mG 

"""
m = [1, 0, 1, 1]


def build_G_Matrix(H_matrix):

    H_matrix = np.array(H_matrix, dtype=int)

    P_transpose = H_matrix[:, : params.k]
    P = P_transpose.T
    I = np.eye(params.k, dtype=int)

    G = np.concatenate((I, P), axis=1)

    return G


G = build_G_Matrix(params.H)

print(G)


def mod_2_dot(a, b):

    a = np.array(a, dtype=int)
    b = np.array(b, dtype=int)

    mod2dot = int(np.dot(a, b) % 2)
    return mod2dot


codeword = mod_2_dot(m, G)
print(codeword)
