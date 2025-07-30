class GraphOptimal1Cycle(object):
    """The class represents an optimal (not volume-optimal) 1-cycle computed from graph information.

    You can aquaire an optimal one cycle by :meth:`Pair.optimal_1_cycle`.

    Examples:
        >>> import numpy as np
        >>> import homcloud.interface as hc
        >>> distance_matrix = np.loadtxt("distance_matrix.txt")
        >>> pdlist = hc.PDList.from_rips_filtration(distance_matrix, maxdim=1, save_graph=True)
        >>> pd1 = pdlist.dth_diagram(1)
        >>> pair = pd1.nearest_pair_to(1.2, 1.5)
        >>> optimal_1_cycle = pair.optimal_1_cycle()
        >>> optimal_1_cycle.boundary_points()
        => [0, 2, 41, 17, 9]
    """

    def __init__(self, pair, path_vertices):
        self.pair = pair
        self.path_vertices = path_vertices

    def birth_time(self):
        """Returns the birth time of the pair.

        Returns:
            float: The birth time
        """
        return self.pair.birth_time()

    def death_time(self):
        """Returns the death time of the pair.

        Returns:
            float: The death time
        """
        return self.pair.death_time()

    def boundary_points(self, by="vertex_indexes"):
        """Returns the points on the 1-cycle.

        Returns:
            list of int: The list of points on the cycle.
            Each point is represented by a number, which is assigned in 0-origin.
        """
        match by:
            case "vertex_indexes" | "vindexes":
                return self.path_vertices
            case "symbols":
                return self.pair.diagram.get_geometry_resolver("symbols").resolve_graph_path(self.path_vertices)
            case _:
                raise ValueError(f"Unknown by: {by}")

    def boundary_points_symbols(self):
        return self.boundary_points("symbols")
