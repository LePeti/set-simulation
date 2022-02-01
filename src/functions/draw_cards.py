import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, RegularPolygon


def draw_cards(cards):
    """Draws one or multiple SET cards on a single plot

    Args:
        cards (list): List of definition of SET cards
        Example: cards=[{"num": 3, "shape": "ellipse", "color": "b", "pattern": "dotted"}]

    Returns:
        None: Draws the plot with cards
    """
    rows = int(np.ceil(len(cards) / 3))
    cols = int(len(cards) if len(cards) <= 2 else 3)
    height = rows * 3
    width = cols * 2
    fig, ax = plt.subplots(rows, cols, figsize=(width, height))
    ax = ax.flatten()
    fig.patch.set_facecolor("w")

    for i, card in enumerate(cards):
        shape_instances = gen_shape_instances(
            card["color"], card["num"], card["shape"], card["pattern"]
        )

        for instance in shape_instances:
            ax[i].add_patch(instance)

        ax[i].set_xlim([0, 2])
        ax[i].set_ylim([0, 3])
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    # removing ticks from remaining empty subplots
    for i in range(len(card), len(ax)):
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    return None


def gen_shape_instances(color, n, shape, pattern):
    properties = get_shape_properties(shape)
    shape_object = properties["shape"]
    shape_instances = []

    if pattern == "empty":
        is_filled = False
        pattern = None
        hatching = None
    elif pattern == "filled":
        is_filled = True
        hatching = None
    elif pattern == "dotted":
        is_filled = False
        hatching = "oo"
    else:
        raise ValueError(f"Incorrect pattern provided: {pattern}")

    if shape in ("rectangle", "ellipse"):
        for position in properties.get(n):
            shape_instance = shape_object(
                xy=(position["x"], position["y"]),
                width=1.5,
                height=0.5,
            )
            shape_instance.set(
                fc=color, edgecolor=color, lw=2, fill=is_filled, hatch=hatching
            )
            shape_instances.append(shape_instance)
    elif shape in ("triangle"):
        for position in properties.get(n):
            shape_instance = shape_object(
                xy=(position["x"], position["y"]),
                numVertices=3,
                radius=0.3,
            )
            shape_instance.set(
                fc=color, edgecolor=color, lw=2, fill=is_filled, hatch=hatching
            )
            shape_instances.append(shape_instance)
    else:
        raise ValueError(f"Incorrect shape provided: {shape}")
    return shape_instances


def get_shape_properties(shape):
    properties = {
        "ellipse": {
            1: [{"x": 1, "y": 1.5}],
            2: [{"x": 1, "y": 1.15}, {"x": 1, "y": 1.85}],
            3: [{"x": 1, "y": 0.75}, {"x": 1, "y": 1.5}, {"x": 1, "y": 2.25}],
            "shape": Ellipse,
        },
        "rectangle": {
            1: [{"x": 0.25, "y": 1.25}],
            2: [{"x": 0.25, "y": 0.9}, {"x": 0.25, "y": 1.6}],
            3: [{"x": 0.25, "y": 0.5}, {"x": 0.25, "y": 1.25}, {"x": 0.25, "y": 2}],
            "shape": Rectangle,
        },
        "triangle": {
            1: [{"x": 1, "y": 1.5}],
            2: [{"x": 1, "y": 1.15}, {"x": 1, "y": 1.85}],
            3: [{"x": 1, "y": 0.75}, {"x": 1, "y": 1.5}, {"x": 1, "y": 2.25}],
            "shape": RegularPolygon,
        },
    }
    return properties[shape]


def translate_vecs_to_cards(vecs):
    card_attribute_values = {
        "shape": ["ellipse", "rectangle", "triangle"],
        "num": [1, 2, 3],
        "color": ["blue", "green", "red"],
        "pattern": ["empty", "filled", "dotted"],
    }
    cards = []
    for vec in vecs:
        card = {
            attr: values[vec[i]]
            for i, (attr, values) in enumerate(card_attribute_values.items())
        }
        cards.append(card)

    return cards
