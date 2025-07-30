import operator

from homcloud.delegate import forwardable
import homcloud.optvol as optvol
import homcloud.paraview_interface as pv_interface
import homcloud.plotly_3d as p3d


@forwardable
class Volume(object):
    """
    This class represents a volume.
    This is the superclass of OptimalVolume, StableVolume and
    StableSubvolume.

    Notes:
        * point: list of float
        * cell: simplex or cube, simplex is used if the filtration is
          simplicial (alpha filtration) and cube is used if the filtration
          is cubical.
        * simplex: list of point
        * cube: tuple[point, list of {0, 1}],
        * ssimplex: list of string
    """

    def __init__(self, pair, cell_indices, result=None):
        self.pair = pair
        self.diagram = pair.diagram
        self.cell_indices = cell_indices
        self.result = result

    __delegator_definitions__ = {"diagram": ["get_geometry_resolver"]}

    def birth_time(self):
        """
        Returns:
            float: The birth time.
        """
        return self.pair.birth_time()

    def death_time(self):
        """
        Returns:
            float: The death time.
        """
        return self.pair.death_time()

    def lifetime(self):
        """
        Returns:
            float: The lifetime of the pair.
        """
        return self.death_time() - self.birth_time()

    def death_position(self, by="default"):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"
        Returns:
            simplex: The death simplex.
        """
        return self.get_geometry_resolver(by).resolve_cell(self.pair.death_index)

    def points(self, by="default"):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"

        Returns:
            list of point: All vertices in the optimal volume.
        """
        return self.get_geometry_resolver(by).resolve_vertices(self.cell_indices)

    def points_symbols(self):
        """
        Returns:
            list of string: All vertices in the optimal volume
            in the form of the symbolic representation.

        Notes:
            This method is the same as :meth:`points` ("symbols")`.
        """
        return self.points("symbols")

    def boundary_points(self, by="default"):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"

        Returns:
            list of point: All vertices in the volume optimal cycle.
        """
        return self.get_geometry_resolver(by).resolve_boundary_vertices(self.cell_indices)

    def boundary_points_symbols(self):
        """
        Returns:
            list of string: All vertices in the volume optimal cycle
            in the form of the symbolic representation.

        Notes:
            This method is the same as :meth:`boundary_points` ("symbols").
        """
        return self.boundary_points("symbols")

    def boundary(self, by="default", adjust_periodic_boundary=None):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"
            adjust_periodic_boundary (Option[(float, float)]): periodic boundary treatment
        Returns:
            list of cells: All cells in the volume optimal cycle.
        """
        return self.get_geometry_resolver(by, adjust_periodic_boundary).resolve_boundary(self.cell_indices)

    def boundary_symbols(self):
        """
        Returns:
            list of ssimplex: All simplices in the volume optimal cycle
            in the form of the symbolic representation.

        Notes:
            This method is the same as :meth:`boundary` ("symbols")
        """
        return self.boundary("symbols")

    def cells(self, by="default", adjust_periodic_boundary=None):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"
            adjust_periodic_boundary (Option[(float, float)]): periodic boundary treatment

        Returns:
            list of cell: All cells in volume optimal cycles.
        """
        return self.get_geometry_resolver(by, adjust_periodic_boundary).resolve_cells(self.cell_indices)

    simplices = cells

    def simplices_symbols(self):
        """
        Returns:
            list of ssimplex: All simplices in volume optimal cycles
            in the form of the symbolic representation.

        Notes:
            This method is the same as :meth:`simplices` ("symbols")
        """
        return self.simplices("symbols")

    volume_simplices_symbols = simplices_symbols

    def cubes(self, by="default"):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"

        Returns:
            list of cube: All cubes in volume optimal cycles.
        """
        return self.cells(by)

    def children(self):
        """
        Returns:
           list of :class:`Pair`: All children pairs.
        """
        from .pd import Pair

        death_to_number = self.diagram.pd.death_index_to_pair_number

        def valid(d):
            return d != self.pair.death_index and d in death_to_number

        return [Pair(self.diagram, death_to_number[d]) for d in self.cell_indices if valid(d)]

    def dump_to_dict(self):
        """Returns information about the optimal volume in the form of dict.
        Users can reconstruct :class:`OptimalVolume` and :class:`StableVolume` from the dictionary
        using :meth:`restore_from_dict`.

        The method is useful to compute large number of optimal/stable volumes.

        Returns:
            dict: The information about the optimal volume.
        """
        assert self.diagram.pdgm_id
        return {
            "type": type(self).__name__,
            "pdgm_id": self.diagram.pdgm_id,
            "degree": self.diagram.degree,
            "nth": self.pair.nth,
            "birth_time": self.pair.birth_time(),
            "death_time": self.pair.death_time(),
            "cell_indices": self.cell_indices,
        }

    @classmethod
    def validate_restore_data(cls, pd, data):
        assert pd.pdgm_id == data["pdgm_id"]
        assert cls.__name__ == data["type"]
        assert pd.degree == data["degree"]

    @classmethod
    def restore_from_dict(cls, pd, data, validate=True):
        """Returns :class:`Volume` object reconstructed from pd and data.
        The data should be a dictionary returned by :meth:`dump_to_dict`.

        This class method should be called with a subclass of Volume,
        :class:`OptimalVolume`, :class:`StableVolume`, or :class:`StableSubvolume`, not Volume class.

        Args:
            pd (:class:`PD`): Persistence diagram object related to the volume
            data (dict): A dictionary which contains volume information
            validate (bool): Validate the information in the dictionary if True

        Returns:
            Volume: restored volume object
        """
        if validate:
            cls.validate_restore_data(pd, data)
        return cls(pd.pair(data["nth"]), data["cell_indices"])

    #: The alias of :meth:`death_position`.
    death_pos = death_position

    def boundary_loop(self, by="default", adjust_periodic_boundary=None):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"
            adjust_periodic_boundary (Option[(float, float)]): periodic boundary treatment

        Returns:
            Optional[list of point]: The list of points in the loop order.
              Return None if the boundary consists of multiple loops.
        Raises:
            ValueError: Raised if the dimension of the volume is not 2D,
              or if the loop is a self-loop or multi-edge loop.
        """
        return self.get_geometry_resolver(by, adjust_periodic_boundary).resolve_boundary_loop(self.cell_indices)

    def boundary_loop_symbols(self):
        """
        Returns:
            Optional[List[str]]: The list of vertex symbols in the loop order.
              Return None if the boundary consists of multiple loops.
        Raises:
            ValueError: Raised if the dimension of the volume is not 2D,
              or if the loop is a self-loop or multi-edge loop.
        """
        return self.boundary_loop("symbols")

    def to_paraview_node(self, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize an optimal volume.

        You can show the optimal volume by
        :meth:`homcloud.paraview_interface.show`. You can also
        adjust the visual by the methods of
        :class:`homcloud.paraview_interface.PipelineNode`.

        Args:
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        return OptimalVolume.to_paraview_node_for_volumes([self], gui_name)

    to_pvnode = to_paraview_node

    @staticmethod
    def to_paraview_node_for_volumes(volumes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize multiple optimal volumes.

        All optimal volumes should come from the same :class:`PD` object.

        Args:
            volumes (list of :class:`OptimalVolume`): The optimal volumes to be
                visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        diagram = volumes[0].diagram
        if diagram.filtration_type == "alpha":
            geom_resolver = diagram.pd.alpha_coord_resolver
            drawer = optvol.drawer_for_alpha(geom_resolver.vertices)
        elif diagram.filtration_type == "cubical":
            geom_resolver = diagram.pd.cubical_geometry_resolver
            drawer = optvol.drawer_for_cubical(geom_resolver.shape)
        optvol.draw_volumes(drawer, map(operator.attrgetter("result"), volumes), geom_resolver)
        f = pv_interface.TempFile(".vtk")
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

    def to_plotly3d_trace(self, color="green", width=1, name=""):
        """
        Constructs a plotly's trace object to visualize the optimal volume

        Args:
            color (string or None): The name of the color
            width (int): The width of the line
            name (string): The name of the object

        Returns:
            plotly.graph_objects.Scatter3d: Plotly's trace object
        """
        if self.diagram.filtration_type == "alpha":
            return p3d.Simplices(self.boundary(), color, width, name)
        elif self.diagram.filtration_type == "cubical":
            return p3d.Cubes(self.boundary(), color, width, name)
        else:
            raise RuntimeError(f"{self.filtration_type} cannot be renderred")

    to_plotly3d = to_plotly3d_trace

    def to_plotly3d_mesh(self, color="green", name=""):
        """
        Constructs a plotly's trace object to visualize the face of an optimal volume

        Args:
            color (string or None): The name of the color
            name (string): The name of the object

        Returns:
            plotly.graph_objects.Mesh3d: Plotly's trace object
        """
        if self.diagram.filtration_type == "alpha":
            if self.diagram.degree == 2:
                return p3d.SimplicesMesh(self.boundary(), color, name)
            elif self.diagram.degree == 1:
                return p3d.SimplicesMesh(self.simplices(), color, name)
            else:
                raise RuntimeError(f"dim {self.diagram.degree} volume is available for plotly")
        elif self.diagram.filtration_type == "cubical":
            if self.diagram.degree == 2:
                return p3d.CubesMesh(self.boundary(), color, name)
        else:
            raise RuntimeError(f"{self.filtration_type} cannot be renderred")

    def to_pyvista_boundary_mesh(self, adjust_periodic_boundary=None):
        """
        Constructs a PyVista's mesh object to visualize the boundary of an optimal/stable volume.
        Args:
            adjust_periodic_boundary (Option[(float, float)]): periodic boundary treatment

        Returns:
            pyvista.PolyData: PyVista's mesh object
        """
        import homcloud.pyvistahelper as pvhelper

        if self.diagram.filtration_type == "alpha":
            if self.diagram.degree == 2:
                return pvhelper.Triangles(self.boundary("coordinates", adjust_periodic_boundary))
            elif self.diagram.degree == 1:
                return pvhelper.Lines(self.boundary("coordinates", adjust_periodic_boundary))
            else:
                raise RuntimeError(f"dim {self.diagram.degree} volume is available for pyvista")

        raise RuntimeError(f"{self.filtration_type} cannot be renderred")

    def to_pyvista_volume_mesh(self, adjust_periodic_boundary=None):
        """
        Constructs a PyVista's mesh object to visualize the internal face of a 1D optimal/stable volume.

        Args:
            adjust_periodic_boundary (Option[(float, float)]): periodic boundary treatment

        Returns:
            pyvista.PolyData: PyVista's mesh object
        """
        import homcloud.pyvistahelper as pvhelper

        if self.diagram.filtration_type == "alpha":
            if self.diagram.degree == 1:
                return pvhelper.Triangles(self.cells("coordinates", adjust_periodic_boundary))
        raise RuntimeError("Volume mesh can only be applied to 1d alpha volume")


class OptimalVolume(Volume):
    """
    This class represents an optimal volume.
    """

    def birth_position(self, by="default"):
        """
        Args:
            by (string): Format of return values, "default", "coordinates", "symbols", "vertex_indexes", or "vindexes"

        Returns:
            simplex: The birth simplex.
        """
        return self.get_geometry_resolver(by).resolve_cell(self.pair.birth_index)

    #: The alias of :meth:`birth_position`.
    birth_pos = birth_position

    def stable_subvolume(self, threshold, solver=None, solver_options=[]):
        """
        Returns the stable subvolume of the optimal volume.

        Args:
            threshold (float): The noise bandwidth.
        Returns:
            StableSubvolume: The stable subvolume.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        ssvfinder = optvol.TightenedSubVolumeFinder(
            self.diagram.optvol_optimizer_builder(None, None, lp_solver), self.diagram.pd.index_to_level, threshold
        )
        result = ssvfinder.find(self.pair.birth_index, self.pair.death_index, self.cell_indices)
        return StableSubvolume(self.pair, result.cell_indices, threshold, result)

    tightened_subvolume = stable_subvolume


class EigenVolume(Volume):
    """
    This class represents an "eigenvolume". It is the superclass of
    StableVolume and StableSubvolume.

    Attributes:
        threshold (float): The threshold used for the computation of the
            eigenvolume.
    """

    def __init__(self, pair, cell_indices, threshold, result=None):
        super().__init__(pair, cell_indices, result)
        self.threshold = threshold

    def dump_to_dict(self):
        data = super().dump_to_dict()
        data["threshold"] = self.threshold
        return data

    @classmethod
    def restore_from_dict(cls, pd, data, validate=True):
        if validate:
            cls.validate_restore_data(pd, data)
        return cls(pd.pair(data["nth"]), data["cell_indices"], data["threshold"])


class StableVolume(EigenVolume):
    """
    This class represents a stable volume.

    The instance is given by :meth:`Pair.stable_volume`.
    """

    pass


class StableSubvolume(EigenVolume):
    """
    This class represents a stable subvolume.

    The instance is given by :meth:`OptimalVolume.stable_subvolume`.
    """

    pass
