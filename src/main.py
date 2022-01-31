import random
from itertools import combinations, product

import numpy as np

# TODO add logging

random.seed(123)


def generate_shuffled_deck():
    deck = list(product(range(3), repeat=4))
    random.shuffle(deck)
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


def remove_set_from_table(table, set_):
    indice_to_remove = []
    for set_card in set_:
        for i, card in enumerate(table):
            if np.array_equal(card, set_card):
                indice_to_remove.append(i)
    return np.delete(table, indice_to_remove, axis=0)


if __name__ == "__main__":
    deck = generate_shuffled_deck()
    deck, table = first_draw(deck)
    removed_sets = []

    while len(deck) != 0:
        # find sets on table
        sets = get_sets_on_table(table)
        num_sets = len(sets)
        # if multiple sets, pick one arbitrarily and add 3 cards from deck
        if num_sets > 0:
            chosen_set = random.choice(sets)
            removed_sets.append(chosen_set)
            table = remove_set_from_table(table, chosen_set)
            deck, table = add_three_cards_to_table(deck, table)
        else:
            deck, table = add_one_card_to_table(deck, table)

    remaining_sets_on_table = get_sets_on_table(table)
    while len(remaining_sets_on_table) > 0:
        chosen_set = random.choice(remaining_sets_on_table)
        removed_sets.append(chosen_set)
        table = remove_set_from_table(table, chosen_set)
        remaining_sets_on_table = get_sets_on_table(table)

    print(f"Remaining cards in deck: {len(deck)}")
    print(f"Remaining cards on table: {len(table)}")
    print(f"Number of sets found: {len(removed_sets)} ({len(removed_sets) * 3} cards)")
