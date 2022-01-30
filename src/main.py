from itertools import product
from random import shuffle

import numpy as np


def generate_shuffled_deck():
    deck = list(product(range(3), repeat=4))
    shuffle(deck)
    return np.array(deck)


if __name__ == "__main__":
    deck = generate_shuffled_deck()
    print(deck)
    print(type(deck))
    print(len(deck))
