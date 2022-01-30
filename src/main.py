from itertools import combinations, product
from random import shuffle

import numpy as np

# TODO add logging


def generate_shuffled_deck():
    deck = list(product(range(3), repeat=4))
    shuffle(deck)
    return np.array(deck)


def draw(deck, n):
    table = deck[:n]
    deck = deck[n:]
    return deck, table


def first_draw(deck):
    return draw(deck, 12)


def get_sets_on_table(table):
    # TODO write tests
    potential_sets = np.array(list(combinations(table, r=3)))
    attribute_sums = potential_sets.sum(axis=1)
    attribute_level_check = np.isin(attribute_sums, [0, 3, 6])
    set_flags = np.all(attribute_level_check, axis=1)
    sets = potential_sets[set_flags]
    return sets


def add_three_cards_to_table(deck, table):
    table = np.concatenate([table, deck[:3]])
    deck = deck[3:]
    return deck, table


def add_one_card_to_table(deck, table):
    table = np.concatenate([table, deck[:1]])
    deck = deck[1:]
    return deck, table


if __name__ == "__main__":
    deck = generate_shuffled_deck()
    deck, table = first_draw(deck)
    while len(deck) != 0:
        # find sets on table
        sets = get_sets_on_table(table)
        num_sets = len(sets)
        # if multiple sets, pick one arbitrarily and add 3 cards from deck
        # if num_sets > 0:

    # elif 0 sets, add 1 card from deck
    # deck is empty, find remaining sets

    # num_sets = 0
    # while num_sets == 0:
    #     deck, table = add_one_card_to_table(deck, table)
