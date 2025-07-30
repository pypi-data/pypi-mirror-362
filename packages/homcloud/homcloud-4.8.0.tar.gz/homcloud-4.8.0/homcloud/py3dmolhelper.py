import numpy as np
import numbers


def ary2v3(ary):
    return {"x": ary[0], "y": ary[1], "z": ary[2]}


def add_edges(view, edges, color, radius, alpha=1.0):
    """
    Add edges to py3dmol view.

    Args:
        view (py3Dmol.view): Py3Dmol's view object
        edges (list[list[list[float]]]): List of edges
        color (str): Name of color
        radius (float): Radius of the cylinders
        alpha (float): Alpha value (1.0: opaque, 0.0: transparent)

    Returns:
        None
    """
    assert isinstance(color, str)
    assert isinstance(radius, numbers.Real)
    assert isinstance(alpha, numbers.Real)

    for edge in edges:
        view.addCylinder(
            {"start": ary2v3(edge[0]), "end": ary2v3(edge[1]), "color": color, "radius": radius, "alpha": alpha}
        )


def add_surface(view, triangles, color, alpha=1.0):
    """
    Add surface (triagnles) to py3dmol view.

    Args:
        view (py3Dmol.view): Py3Dmol's view object
        triangles (list[list[list[float]]]): List of triangles
        color (str): Name of color
        alpha (float): Alpha value (1.0: opaque, 0.0: transparent)
    """
    assert isinstance(color, str)
    assert isinstance(alpha, numbers.Real)

    for cell in triangles:
        normal = ary2v3(np.cross(np.array(cell[1]) - cell[0], np.array(cell[2]) - cell[0]))
        view.addCustom(
            {
                "vertexArr": [ary2v3(cell[0]), ary2v3(cell[1]), ary2v3(cell[2])],
                "normalArr": [normal, normal, normal],
                "faceArr": [0, 1, 2],
                "color": color,
                "alpha": alpha,
            }
        )
