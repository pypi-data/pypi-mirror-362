from random import random


def random_byte_array():
    # type: () -> bytearray
    byte_array = bytearray()
    while True:
        random_byte_or_eos = int(random() * 257)
        if random_byte_or_eos < 256:
            byte_array.append(random_byte_or_eos)
        else:
            return byte_array