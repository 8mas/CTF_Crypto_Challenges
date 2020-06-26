import sympy

"""
Solution for RSAService Challange @CSCG2020 - Small but interesting RSA challenge.
"""

message = b"Quack! Quack!"
question_to_ask = b"Hello! Can you give me the flag, please? I would really appreciate it!"

target_Number = int.from_bytes(question_to_ask, "big")
start_Number = int.from_bytes(message, "big")


def generate_smooth_integer(n=100):
    """
    Generates an n smooth integer
    """

    p = 2
    q = 2
    while p * q < target_Number:
        p *= sympy.randprime(2, n)
    return p


def generate_smooth_prime(n=100):
    """
    Generates an n smooth prime
    """

    p = generate_smooth_integer(n)
    while not (sympy.isprime(p + 1)):
        p = generate_smooth_integer(n)
    return p + 1


def generate_parameters():
    """
    Generates an p, q and n where the discrete log, and therefore the exponent e can be calculated with Pohlig-Hellman.
    An e is selected which has an inverse modulo N.
    :return: p, q, e, d
    """

    p = 0
    q = 2
    e = 0
    d = 0

    no_primitive_root_and_inverse = True
    while no_primitive_root_and_inverse:
        p = generate_smooth_prime()
        N = p * q

        try:
            e = sympy.discrete_log(N, start_Number, target_Number)
            d = sympy.mod_inverse(e, (p-1) * (q-1))  # Euler
            no_primitive_root_and_inverse = False

        except ValueError:
            # No primitive root for this N or no inverse for e mod N
            pass

    return p, q, e, d


def test_solution(p, q, e, d):
    if pow(target_Number, e, p * q) == start_Number and pow(start_Number, d, p * q) == target_Number:
        print("Solution seems correct")


if __name__ == '__main__':
    print("target", target_Number)
    print("start", start_Number)

    p, q, e, d = generate_parameters()

    print("N: ", p*q)
    print("p: ", p)
    print("q: ", q)
    print("e: ", e)
    print("d: ", d)
    test_solution(p, q, e, d)