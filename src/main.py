import logging
import random
from datetime import datetime
from itertools import combinations, product

import numpy as np
import pandas as pd
import os
from src.functions.draw_cards import draw_cards, translate_vecs_to_cards

random.seed(123)
logging.basicConfig(level=logging.WARNING)


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
    if len(table) == 0:
        return np.array([])
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


def get_simul_data_col_names():
    return [
        "game_id",
        "round_id",
        "round_type",
        "is_first_round",
        "is_last_round",
        "datetime",
        "num_cards_table",
        "num_cards_deck",
        "num_sets",
        "cards_table",
        "cards_deck",
        "sets",
        "chosen_set",
    ]


if __name__ == "__main__":
    simul_data = pd.DataFrame(columns=get_simul_data_col_names())
    game_id = 0
    for game in range(1):
        logging.warning(f"Game simulation round #{game + 1} ({game + 1:.0f}%)")
        game_id += 1
        deck = generate_shuffled_deck()
        deck, table = first_draw(deck)
        logging.info(f"{len(table)} cards on the table.")

        removed_sets = []
        game_data = pd.DataFrame(columns=get_simul_data_col_names())
        is_last_round = False
        round_id = 0

        while len(deck) != 0:
            round_id += 1
            logging.info(f"\n\n-~=ROUND #{round_id}=~-\n")
            logging.info(f"Num cards in deck/table: {len(deck)}/{len(table)}.")
            sets = get_sets_on_table(table)
            num_sets = len(sets)
            logging.info(f"Found {num_sets} SET(s) on the table.")
            round_data = pd.DataFrame(
                {
                    "game_id": [game_id],
                    "round_id": [round_id],
                    "is_first_round": [round_id == 1],
                    "is_last_round": [is_last_round],
                    "datetime": [datetime.utcnow().isoformat()],
                    "num_cards_table": [len(table)],
                    "num_cards_deck": [len(deck)],
                    "num_sets": [num_sets],
                    "cards_table": [[table]],
                    "cards_deck": [[deck]],
                    "sets": [[sets]],
                }
            )
            if num_sets > 0:
                round_data["round_type"] = "normal"
                chosen_set = random.choice(sets)
                round_data["chosen_set"] = [chosen_set]
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
                round_data["round_type"] = "no-set"
                round_data["chosen_set"] = [sets]
                deck, table = add_n_cards_to_table(deck, table, 1)
                logging.info("No sets found on the table, adding 1 card.")
            game_data = pd.concat([game_data, round_data], ignore_index=True)

        logging.info("No more cards in deck.")
        logging.info(f"Remaining cards on table: {len(table)}.")
        logging.info("Looking for remaining sets on table.")
        remaining_sets_on_table = get_sets_on_table(table)

        while len(remaining_sets_on_table) > 0:
            round_id += 1
            round_data = pd.DataFrame(
                {
                    "game_id": [game_id],
                    "round_id": [round_id],
                    "is_first_round": [round_id == 1],
                    "is_last_round": [False],
                    "datetime": [datetime.utcnow().isoformat()],
                    "num_cards_table": [len(table)],
                    "num_cards_deck": [len(deck)],
                    "num_sets": [len(remaining_sets_on_table)],
                    "cards_table": [[table]],
                    "cards_deck": [[deck]],
                    "sets": [[remaining_sets_on_table]],
                }
            )
            logging.info("Found one, looking for more.")
            chosen_set = random.choice(remaining_sets_on_table)
            removed_sets.append(chosen_set)
            table = remove_set_from_table(table, chosen_set)
            remaining_sets_on_table = get_sets_on_table(table)
            round_data["chosen_set"] = [chosen_set]
            round_data["round_type"] = "no-deck"
            game_data = pd.concat([game_data, round_data], ignore_index=True)

        round_id += 1
        round_data = pd.DataFrame(
            {
                "game_id": [game_id],
                "round_id": [round_id],
                "is_first_round": [round_id == 1],
                "round_type": ["no-deck"],
                "datetime": [datetime.utcnow().isoformat()],
                "num_cards_table": [len(table)],
                "num_cards_deck": [len(deck)],
                "num_sets": 0,
                "cards_table": [[table]],
                "cards_deck": [[deck]],
                "sets": [[remaining_sets_on_table]],
            }
        )
        round_data["is_last_round"] = True
        round_data["chosen_set"] = [remaining_sets_on_table]
        game_data = pd.concat([game_data, round_data], ignore_index=True)

        draw_cards(translate_vecs_to_cards(table), "Cards left on the table w/o any SETs")
        logging.info("No more cards in deck, no more sets on table.")

        logging.info(f"Remaining cards in deck: {len(deck)}.")
        logging.info(f"Remaining cards on table: {len(table)}.")
        logging.info(
            f"Number of sets found: {len(removed_sets)} "
            f"({len(removed_sets) * 3} cards.)"
        )
        simul_data = pd.concat([simul_data, game_data], ignore_index=True)

    time_ = datetime.now()
    data_file_name = f"set_simul_{time_.strftime('%Y%m%d')}_{time_.strftime('%f')}.pkl"
    artifacts_folder = os.path.join("artifacts", data_file_name)
    simul_data.to_pickle(artifacts_folder)
