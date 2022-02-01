from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, RegularPolygon


def draw_n_shape(color, n, shape):
    shape_properties = get_shape_properties(shape)
    shape_instances = gen_shape_instances(color, n, shape)

    fig, ax = plt.subplots(figsize=(2, 3))
    for instance in shape_instances:
        ax.add_patch(instance)

    ax.set_xlim([0, 2])
    ax.set_ylim([0, 3])
    plt.xticks(ticks=[], labels=[])
    plt.yticks(ticks=[], labels=[])

    return None


def gen_shape_instances(color, n, shape):
    properties = get_shape_properties(shape)
    shape_object = properties["shape"]
    shape_instances = []
    if shape in ("rectangle", "ellipse"):
        for position in properties.get(n):
            shape_instance = shape_object(
                xy=(position["x"], position["y"]),
                width=1.5,
                height=.5,
                edgecolor=color,
                fc=color,
                lw=0,
            )
            shape_instances.append(shape_instance)
    elif shape in ("triangle"):
        for position in properties.get(n):
            shape_instance = shape_object(
                xy=(position["x"], position["y"]),
                numVertices=3,
                radius=0.3,
                edgecolor=color,
                fc=color,
                lw=0,
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
            3: [{"x": 0.25, "y": .5}, {"x": 0.25, "y": 1.25}, {"x": 0.25, "y": 2}],
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


draw_n_shape("b", 3, "triangle")
draw_n_shape("b", 2, "triangle")
draw_n_shape("b", 1, "triangle")

# ellipse
# triangle
