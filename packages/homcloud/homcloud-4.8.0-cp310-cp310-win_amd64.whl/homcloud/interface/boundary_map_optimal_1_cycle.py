from homcloud.paraview_interface import SparseCubeDrawer, SimplexDrawer
import homcloud.paraview_interface as pv_interface
import homcloud.plotly_3d as p3d


class Optimal1Cycle(object):
    """The class represents an optimal (not volume-optimal) 1-cycle.

    This class is available only for alpha, cubical, rips, and abstract filtration
    with boundary map information.

    You can aquaire an optimal one cycle by :meth:`Pair.optimal_1_cycle`.
    """

    def __init__(self, pair, path):
        self.pair = pair
        self.path_edges = path

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

    def birth_position(self):
        """Birth position of the birth-death pair"""
        return self.pair.birth_position

    def path(self, by="default"):
        """
        Returns:
            list of cell: All edges in the optimal 1-cycle.
        """
        return self.get_geometry_resolver(by).resolve_cells(self.path_edges)

    def path_symbols(self):
        """
        Returns:
            list of ssimplex: All edges in the optimal 1-cycle
            in the form of the symbolic representation.
        """
        return self.path("symbols")

    def boundary_points(self, by="default"):
        """
        Returns:
            list of point: All vertices in the optimal 1-cycle.
        """
        return self.get_geometry_resolver(by).resolve_vertices(self.path_edges)

    def boundary_points_symbols(self):
        """
        Returns:
            list of string: All vertices in the optimal 1-cycle
            in the form of the symbolic representation.
        """
        return self.boundary_points("symbols")

    def get_geometry_resolver(self, by="default"):
        return self.pair.diagram.get_geometry_resolver(by)

    def to_paraview_node(self, gui_name=None):
        geom_resolver = self.get_geometry_resolver("coordinates")

        if self.pair.diagram.filtration_type == "cubical":
            drawer = SparseCubeDrawer(1, 3, {"isboundary": "1"})
        elif self.pair.diagram.filtration_type == "alpha":
            drawer = SimplexDrawer(1, geom_resolver.vertices, {"isboundary": "1"})
        else:
            raise RuntimeError("Unsupported filtration type")

        drawer.draw_cells(geom_resolver, self.path_edges, drawer.various_colors[0])

        f = pv_interface.TempFile(".vtk")
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

    to_pvnode = to_paraview_node

    def to_plotly3d_trace(self, color=None, width=1, name=""):
        """
        Constructs a plotly's trace object to visualize the optimal 1-cycle

        Args:
            color (string or None): The name of the color
            width (int): The width of the lines
            name (string): The name of the object

        Returns:
            plotly.graph_objects.Scatter3d: Plotly's trace object
        """
        if self.filtration_type == "alpha":
            return p3d.Simplices(self.path(), color, width, name)
        elif self.filtration_type == "cubical":
            return p3d.Cubes(self.path(), color, width, name)
        else:
            raise RuntimeError(f"Unsupported filtration type {self.filtration_type} for plotly3d")

    to_plotly3d = to_plotly3d_trace

    def to_pyvista_mesh(self):
        """
        Constructs a PyVista's mesh object to visualize the optimal 1-cycle.

        Returns:
            pyvista.PolyData: PyVista's mesh object
        """
        import homcloud.pyvistahelper as pvhelper

        if self.filtration_type == "alpha":
            return pvhelper.Lines(self.path())
        raise RuntimeError(f"Unsupported filtration type {self.filtration_type} for pyvista")

    @property
    def filtration_type(self):
        return self.pair.diagram.filtration_type
