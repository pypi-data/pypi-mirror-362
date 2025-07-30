import numpy as np

import homcloud.phtrees as phtrees
import homcloud.paraview_interface as pv_interface
import homcloud.plotly_3d as p3d
from homcloud.spatial_searcher import SpatialSearcher


class PHTrees(object):
    """
    This class represents PH trees computed from an alpha filtration.

    Please see `Obayashi (2018) <https://doi.org/10.1137/17M1159439>`_ if you want to know
    more about optimal volumes, and see `Obayashi (2023) <https://doi.org/10.1007/s41468-023-00119-8>`_
    if you want to know more about stable volumes.

    You can compute the PH trees by :meth:`PDList.from_alpha_filtration`
    with ``save_boundary_map=True`` and ``save_phtrees=True`` arguments.

    .. You can compute the PH trees by :meth:`PD.phtrees` from the diagram.

    Example:
        >>> import homcloud.interface as hc
        >>> pointcloud = hc.example_data("tetrahedron")
        >>> # Compute PDs and PHTrees
        >>> pdlist = hc.PDList.from_alpha_filtration(pointcloud, save_boundary_map=True, save_phtrees=True)
        >>> # Load phtrees
        >>> phtrees = pdlist.dth_diagram(2).load_phtrees()
        >>> # Query the node whose birth-death pair is nearest to (19, 21).
        >>> node = phtrees.pair_node_nearest_to(19, 21)
        >>> # Show birth time and death time
        >>> node.birth_time()
        19.600000000000005
        >>> node.death_time()
        21.069444444444443
        >>> node.boundary_points()
        [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]]
        >>> node.boundary()
        [[[0.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0]],
         [[8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [4.0, 2.0, 6.0]]]

    """

    def __init__(self, orig, spatial_searcher):
        self.orig = orig
        self.spatial_searcher = spatial_searcher

    @staticmethod
    def from_pdgm(pdgm):
        return PHTrees(
            phtrees.PHTrees.from_pdgm(pdgm, PHTrees.Node),
            SpatialSearcher(pdgm.death_indices, pdgm.births, pdgm.deaths),
        )

    @property
    def all_nodes(self):
        """
        Return all nodes.

        Returns:
            list[:class:`PHTrees.Node`]: The nodes.
        """
        return list(self.orig.nodes.values())

    @property
    def roots(self):
        return self.orig.roots

    def nodes_of(self, pairs):
        """
        Returns the nodes of trees corresponding to birth-death pairs
        in `pairs`.

        Args:
            pairs (list[Pair]): The list of pairs.

        Returns:
            list[:class:`PHTrees.Node`]: The nodes.
        """
        return [self._resolver().phtree.nodes[pair.death_index] for pair in pairs]

    def pair_node_nearest_to(self, x, y):
        """
        Return the node corresponding the pair which is nearest to
        (`x`, `y`).

        Args:
            x (float): The birth-axis coordinate.
            y (float): The death-axis coordinate.

        Returns:
            :class:`PHTrees.Node`: The nearest node.

        """
        return self.orig.nodes[self.spatial_searcher.nearest_pair(x, y)]

    def pair_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        """
        Returns the list of nodes corresponding to the birth-death
        pairs in the given rectangle.

        Args:
           xmin (float): The minimum of the birth-axis of the rectangle.
           xmax (float): The maximum of the birth-axis of the rectangle.
           ymin (float): The minimum of the death-axis of the rectangle.
           ymax (float): The maximum of the death-axis of the rectangle.

        Returns:
           list[:class:`PHTrees.Node`]: The nodes in the rectangle.

        """
        return [
            self.orig.nodes[death_index] for death_index in self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)
        ]

    @staticmethod
    def _to_paraview_node_from_nodes(all_vertices, nodes, gui_name=None):
        f = pv_interface.TempFile(".vtk")
        drawer = pv_interface.SimplexDrawer(len(nodes), all_vertices, {})
        for i, node in enumerate(nodes):
            node.draw_volume(drawer, i)
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

    def to_paraview_node_from_nodes(self, nodes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode`
        object to visulize optimal volumes of the nodes.

        Args:
            nodes (list[:class:`PHTrees.Node`]): The list of nodes to be visualized.
            gui_name (str | None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.VTK: Paraview Pipeline node object.

        Notes:
            All nodes should be nodes of `self` PHTrees.
        """
        return self._to_paraview_node_from_nodes(self.orig.coord_resolver.vertices, nodes, gui_name)

    to_pvnode_from_nodes = to_paraview_node_from_nodes

    class Volume(object):
        """
        The superclass of :class:`PHTrees.Node` and :class:`PHTrees.StableVolume`.

        Methods:
            birth_time()
                Returns:
                    float: The birth time of the corresponding birth-death pair.

            death_time()
                Returns:
                    float: The death time of the corresponding birth-death pair.

            lifetime()
                Returns:
                    float: The lifetime of the corresponding birth-death pair.

            simplices()
                Returns:
                    list[list[list[float]]], a.k.a list[Simplex]:
                        The simplices in the optimal volume.

            boundary()
                Returns:
                    list[list[float]], a.k.a. list[Point]:
                        Points in the volume optimal cycle.

            birth_simplex()
                Returns the birth simplex.

            death_simplex()
                Returns the death simplex.

            ancestors()
                Returns:
                    list[:class:`PHTrees.Node`]:
                        The ancestors of the tree node include itself.
        """

        def points(self):
            """
            Returns:
                list[list[float]], a.k.a list[Point]:
                    Points in the optimal volume.
            """
            return self.vertices()

        def volume(self):
            return self.volume_nodes

        def boundary_points(self):
            """
            Returns:
                list[list[float]]: All vertices in the boundary of the optimal/stable volume
            """
            return self.boundary_vertices()

        def points_symbols(self):
            """
            Returns:
                list[str]: All vertices in the optimal/stable volume
                in the form of the symbolic representation.
            """
            return self.vertices("symbols")

        def volume_simplices_symbols(self):
            """
            Returns:
                list[list[str]]: All simplices in optimal/stable volume
                in the form of the symbolic representation.
            """
            return self.simplices("symbols")

        def boundary_points_symbols(self):
            """
            Returns:
                list[str]: All vertices in the boundary of the optimal/stable volume
                in the form of the symbolic representation.
            """
            return self.boundary_vertices("symbols")

        def boundary_symbols(self):
            """
            Returns:
                list[list[str]]: All simplices in the optimal/stable volume
                in the form of the symbolic representation.
            """
            return self.boundary("symbols")

        def living(self):
            """
            Returns:
                bool: True if the birth time and death time of the node
                are different.
            """
            return self.birth_time() != self.death_time()

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode`
            object to visulize an optimal/stable volume of the node.

            gui_name (str | None): The name shown in Pipeline Browser
                in paraview's GUI.

            Returns:
                homcloud.paraview_interface.VTK: Paraview Pipeline node object.
            """
            return PHTrees._to_paraview_node_from_nodes(self.trees.coord_resolver.vertices, [self], gui_name)

        to_pvnode = to_paraview_node

        def to_plotly3d_trace(self, color="green", width=1, name=""):
            """
            Constructs a plotly's trace object to visualize the optimal volume

            Args:
                color (str | None): The name of the color
                width (int): The width of the line
                name (str): The name of the object

            Returns:
                plotly.graph_objects.Scatter3d: Plotly's trace object
            """
            return p3d.Simplices(self.boundary(), color, width, name)

        to_plotly3d = to_plotly3d_trace

        def to_plotly3d_mesh(self, color="green", name=""):
            """
            Constructs a plotly's trace object to visualize the face of an optimal/stable volume

            Args:
                color (str | None): The name of the color
                name (str): The name of the object

            Returns:
                plotly.graph_objects.Mesh3d: Plotly's trace object
            """
            return p3d.SimplicesMesh(self.boundary(), color, name)

        def to_pyvista_mesh(self):
            """
            Constructs a PyVista's mesh object to visualize the face of an optimal/stable volume

            Returns:
                pyvista.PolyData: PyVista's mesh object
            """
            import homcloud.pyvistahelper as pvhelper

            return pvhelper.Triangles(self.boundary())

    class Node(Volume, phtrees.Node):
        """
        The class represents a tree node of :class:`PHTrees`. A node have information about an optimal volume.
        """

        def ancestors(self):
            ret = [self]
            while True:
                parent = self.trees.parent_of(ret[-1])
                if parent is None:
                    break
                ret.append(parent)

            return ret

        def living_descendants(self):
            """
            Returns:
                list[:class:`PHTrees.Node`]: All descendant nodes with positive lifetime
            """
            return [node for node in self.volume_nodes if node.living()]

        def stable_volume(self, epsilon):
            """
            Returns the stable volume corresponding to self.

            Args:
                epsilon (float): Duration noise strength

            Returns:
                :class:`PHTrees.StableVolume`: The stable volume

            """
            return super().stable_volume(epsilon, PHTrees.StableVolume)

        def stable_volume_information(self):
            thresholds = np.array([child.birth_time() - self.birth_time() for child in self.children])
            volumes = np.array([child.volume_size() for child in self.children])
            return (thresholds, volumes)

        def __repr__(self):
            return "PHTrees.Node({}, {})".format(self.birth_time(), self.death_time())

    class StableVolume(Volume, phtrees.StableVolume):
        """
        The class represents a stable volume in :class:`PHTrees`.
        """

        pass
