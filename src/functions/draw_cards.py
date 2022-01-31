from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, RegularPolygon


def draw_n_shape(color, n, shape):
    shape_properties = get_shape_properties(shape)
    shape_instances = gen_shape_instances(color, n, shape)

    fig, ax = plt.subplots(figsize=(2, 3))
    for instance in shape_instances:
        ax.add_patch(instance)

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
                width=0.7,
                height=0.2,
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
                radius=0.1,
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
            1: [{"x": 0.5, "y": 0.5}],
            2: [{"x": 0.5, "y": 0.35}, {"x": 0.5, "y": 0.65}],
            3: [{"x": 0.5, "y": 0.25}, {"x": 0.5, "y": 0.5}, {"x": 0.5, "y": 0.75}],
            "shape": Ellipse,
        },
        "rectangle": {
            1: [{"x": 0.15, "y": 0.4}],
            2: [{"x": 0.15, "y": 0.25}, {"x": 0.15, "y": 0.55}],
            3: [{"x": 0.15, "y": 0.15}, {"x": 0.15, "y": 0.4}, {"x": 0.15, "y": 0.65}],
            "shape": Rectangle,
        },
        "triangle": {
            1: [{"x": 0.5, "y": 0.5}],
            2: [{"x": 0.5, "y": 0.35}, {"x": 0.5, "y": 0.65}],
            3: [{"x": 0.5, "y": 0.25}, {"x": 0.5, "y": 0.5}, {"x": 0.5, "y": 0.75}],
            "shape": RegularPolygon,
        },
    }
    return properties[shape]


# draw_n_shape("g", 3, "rectangle")
# draw_n_shape("b", 2, "ellipse")
# draw_n_shape("r", 3, "triangle")
