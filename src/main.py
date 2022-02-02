import logging
import random
from itertools import combinations, product

import numpy as np
from functions.draw_cards import draw_cards, translate_vecs_to_cards

random.seed(123)
logging.basicConfig(level=logging.INFO)


def generate_shuffled_deck():
    deck = list(product(range(3), repeat=4))
    random.shuffle(deck)
    logging.info(f"Shuffled deck generated with {len(deck)} cards.")
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


def add_n_cards_to_table(deck, table, n):
    table = np.concatenate([table, deck[:n]])
    deck = deck[n:]
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
    logging.info(f"{len(table)} cards on the table.")
    removed_sets = []
    round_ = 0

    while len(deck) != 0:
        round_ += 1
        # find sets on table
        logging.info(f"\n\n-~=ROUND #{round_}=~-\n")
        logging.info(f"Num cards in deck/table: {len(deck)}/{len(table)}.")
        sets = get_sets_on_table(table)
        num_sets = len(sets)
        logging.info(f"Found {num_sets} SET(s) on the table.")
        # if multiple sets, pick one arbitrarily and add 3 cards from deck
        if num_sets > 0:
            chosen_set = random.choice(sets)
            draw_cards(translate_vecs_to_cards(chosen_set))
            removed_sets.append(chosen_set)
            table = remove_set_from_table(table, chosen_set)
            deck, table = add_n_cards_to_table(deck, table, 12 - len(table))
            logging.info(
                f"Chosen set: \n {chosen_set} \n\n"
                f"(total SETs so far: {len(removed_sets)})"
            )
            logging.info("Adding new cards from deck.")
        else:
            deck, table = add_n_cards_to_table(deck, table, 1)
            logging.info("No sets found on the table, adding 1 card.")
    logging.info("No more cards in deck.")
    logging.info(f"Remaining cards on table: {len(table)}.")

    logging.info("Looking for remaining sets on table.")
    remaining_sets_on_table = get_sets_on_table(table)
    while len(remaining_sets_on_table) > 0:
        logging.info("Found one, looking for more.")
        chosen_set = random.choice(remaining_sets_on_table)
        removed_sets.append(chosen_set)
        table = remove_set_from_table(table, chosen_set)
        remaining_sets_on_table = get_sets_on_table(table)

    draw_cards(translate_vecs_to_cards(table), "Cards left on the table w/o any SETs")
    logging.info("No more cards in deck, no more sets on table.")

    logging.info(f"Remaining cards in deck: {len(deck)}.")
    logging.info(f"Remaining cards on table: {len(table)}.")
    logging.info(
        f"Number of sets found: {len(removed_sets)} " f"({len(removed_sets) * 3} cards.)"
    )
