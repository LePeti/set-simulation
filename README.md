# Set simulation

> Set is a fun cardgame
## Game flow
![game-flow](game-flow.png)

## Columns of SET simulation data

1. `game_id` - the ID of a complete game of SET
2. `round_id` - the ID of a round in SET which includes looking for SETs, removing one (if any) and replacing the removed cards from the deck (if any). `game_id` and `round_id` are the keys of the table.
3. `round_type` - one of three types:
   1. `normal` - deck not empty, at least 1 SET found
   2. `no-set` - deck not empty, no SETs found
   3. `no-deck` - deck empty, looking for set
4. `is_first_round` - True if first round, False otherwise
5. `is_last_round` - True if last round, False otherwise
6. `date_time`
8. `num_cards_table` - number of cards on the table at the beginning of the round
9. `num_cards_deck` - number of cards in the deck at the beginning of the round
10. `num_sets` - number of SETs at the beginning of the round
11. `cards_table` - cards on the table
12. `cards_deck` - cards in the deck
13. `sets` - cards of SETs grouped
14. `chosen_set`
