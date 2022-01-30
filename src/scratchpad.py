from main import *
from random import seed


seed(121)

# a_set = np.array([
#     [0, 0, 0, 0],
#     [0, 1, 1, 2],
#     [0, 2, 2, 1]
# ])

deck = generate_shuffled_deck()
_, table = draw(deck, 2)
print(f"number of cards on the table: {len(table)}")
table = np.concatenate([a_set, table])
# print(table)
sets = get_sets_on_table(table)
print(f"sets type: {type(sets)}, shape: {sets.shape}")
print(f"number of sets: {len(sets)}")
print(sets)


# return np.array(
#     deck, dtype=[("shape", "i4"), ("num", "i4"), ("color", "i4"), ("pattern", "i4")]
# )
