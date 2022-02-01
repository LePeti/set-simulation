from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, RegularPolygon


def draw_n_shape(color, n, shape, pattern):
    shape_instances = gen_shape_instances(color, n, shape, pattern)

    fig, ax = plt.subplots(figsize=(2, 3))
    for instance in shape_instances:
        ax.add_patch(instance)

    ax.set_xlim([0, 2])
    ax.set_ylim([0, 3])
    plt.xticks(ticks=[], labels=[])
    plt.yticks(ticks=[], labels=[])

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
            ),
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


draw_n_shape("b", 3, "rectangle", "filled")
draw_n_shape("b", 2, "ellipse", "dotted")
draw_n_shape("b", 1, "triangle", "empty")
