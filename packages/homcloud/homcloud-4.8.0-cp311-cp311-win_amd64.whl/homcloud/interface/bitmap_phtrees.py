import numpy as np

import homcloud.pict.tree as pict_tree
import homcloud.paraview_interface as pv_interface
import homcloud.plotly_3d as p3d
from homcloud.spatial_searcher import SpatialSearcher
from . import bitmap as bm


class BitmapPHTrees(object):
    """
    This class represents PH trees computed from a bitmap filtration.

    You can create an instance of this class by :meth:`PDList.bitmap_phtrees`.

    Please see `Obayashi (2018) <https://doi.org/10.1137/17M1159439>`_ if you want to know
    more about optimal volumes, and see `Obayashi (2023) <https://doi.org/10.1007/s41468-023-00119-8>`_
    if you want to know more about stable volumes.


    Attributes:
        nodes (list of :class:`BitmapPHTrees.Node`): All nodes
        essential_nodes (list of :class:`BitmapPHTrees.Node`): All essential nodes
        nonessential_nodes (list of :class:`BitmapPHTrees.Node`): All nonessential nodes
        roots (list of :class:`BitmapPHTrees.Node`): All root nodes
    """

    @staticmethod
    def for_bitmap_levelset(array, mode="sublevel", save_to=None):
        """Computes a PH trees from 0-th and (n-1)-st persistent homology
        from levelset filtration of the bitmap.

        Args:
            array (numpy.ndarray): The bitmap data.
            mode (string): "superlevel" or "sublevel".
            save_to (string or None): The filepath which the
                PH trees is stored in.

        Returns:
            :class:`PDList`: The 0th and (n-1)st PDs with PH-trees.
        """
        from .pd import PDList

        is_superlevel = mode == "superlevel"
        lower, upper = pict_tree.construct_mergetrees(array, is_superlevel)

        f = PDList.open_pdgm_file(save_to)
        pict_tree.save_pdgm(f, array.ndim, is_superlevel, lower, upper)
        f.seek(0)
        return PDList(f, PDList.FileType.PDGM)

    def __init__(self, treedict, is_superlevel):
        self.treedict = treedict
        self.is_superlevel = is_superlevel

        self.nodes = [self.node(id) for id in self.treedict["nodes"] if not self.is_trivial_id(id)]
        self.essential_nodes = [node for node in self.nodes if node.essential()]
        self.nonessential_nodes = [node for node in self.nodes if not node.essential()]
        self.spatial_searcher = self.build_spatial_searcher()
        self.roots = [node for node in self.nodes if node.isroot()]

    def node(self, id):
        return BitmapPHTrees.Node(self, self.treedict["nodes"][id])

    def is_trivial_id(self, id):
        node = self.treedict["nodes"][id]
        return node["birth-time"] == node["death-time"]

    def build_spatial_searcher(self):
        births = np.array([node.birth_time() for node in self.nonessential_nodes])
        deaths = np.array([node.death_time() for node in self.nonessential_nodes])
        return SpatialSearcher(self.nonessential_nodes, births, deaths)

    def degree(self):
        """
        Returns:
            int: The degree of the persistent homology.
        """
        return self.treedict["degree"]

    def nearest_pair_node(self, x, y):
        """
        Searches a tree node corresponding the birth-death pair
        nearest to (x, y).

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        Returns:
            :class:`BitmapPHTrees.Node`: The node.
        """
        return self.spatial_searcher.nearest_pair(x, y)

    def pair_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        """
        Searches tree nodes corresponding the birth-death pairs
        which the given rectangle contains.

        Args:
            xmin (float): The left side of the rectangle.
            xmax (float): The right side of the rectangle.
            ymin (float): The bottom side of the rectangle.
            ymax (float): The top side of the rectangle.

        Returns:
            list of :class:`BitmapPHTrees.Node`: The nodes.
        """

        return self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)

    def sign(self):
        return -1 if self.is_superlevel else 1

    class Volume(object):
        """
        This class is the superclass of :class:`Node` and :class:`StableVolume`.

        This class defines common methods for these two classes.
        """

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode` object
            to visulize :meth:`volume`.

            You can show the volume by
            :meth:`homcloud.paraview_interface.show`. You can also
            adjust the visual by the methods of
            :class:`homcloud.paraview_interface.PipelineNode`.

            Args:
                gui_name (string or None): The name shown in Pipeline Browser
                    in paraview's GUI.

            Returns:
                homcloud.paraview_interface.PipelineNode: A PipelineNode object.
            """
            return BitmapPHTrees.to_paraview_node_from_nodes([self], gui_name)

        to_pvnode = to_paraview_node

        def to_plotly3d_trace(self, color=None, name=""):
            """
            Constructs a plotly's trace object to visualize the volume

            Args:
                color (string or None): The name of the color
                name (string): The name of the object

            Returns:
                plotly.graph_objects.Mesh3d: Plotly's trace object
            """
            return p3d.Voxels(self.volume(), color, name)

        to_plotly3d = to_plotly3d_trace

        def to_pyvista_mesh(self):
            """
            Constructs a PyVista's mesh object to visualize an optimal/stable volume

            Returns:
                pyvista.PolyData: PyVista's mesh object
            """
            import homcloud.pyvistahelper as pvhelper

            return pvhelper.SparseVoxels(self.volume())

    class Node(Volume):
        """
        This class represents a tree node of PH trees for a bitmap filtration.

        You can draw the optimal volume corresponding to the node
        on an image by :meth:`draw_volumes_on_2d_image`.
        """

        def __init__(self, mt, dic):
            self.mt = mt
            self.dic = dic

        def birth_time(self):
            """
            Returns:
                float: The birth time.
            """
            return self.dic["birth-time"]

        def death_time(self):
            """
            Returns:
                float: The death time. May be infinity.
            """
            if not self.essential():
                return self.dic["death-time"]
            return self.mt.sign() * np.inf

        def lifetime(self):
            """
            Returns:
                float: The lifetime of the pair.
            """
            return self.death_time() - self.birth_time()

        def __iter__(self):
            return (self.birth_time(), self.death_time()).__iter__()

        def birth_position(self):
            """Returns the birth pixel.

            Returns:
               list of int: The coordinate of the birth pixel.
            """
            return self.dic["birth-pixel"]

        birth_pixel = birth_position

        def death_position(self):
            """Returns the death pixel.

            Returns:
               list of int: The coordinate of the death pixel.
            """
            return self.dic["death-pixel"]

        death_pixel = death_position

        def volume(self):
            """
            Returns the optimal volume.

            In fact, for degree 0 node, this method returns
            optimal 0-cohomological volume (this means
            maximal connected conponents in the filtration)
            and for degree (n-1),
            this method returns optimal (n-1)-homological volume.
            This fact is quite mathematical problem, so if you feel that
            it is too difficult to understand, you can ignore the fact.
            You can understand the volume information without the understanding
            of such mathematical background.

            Returns:
                list of list of int: The coordinates of all pixels
                in the optimal volume.
            """
            return self.dic["volume"]

        def stable_volume(self, epsilon):
            """
            Returns the stable volume of the optimal volume with parameter epsilon.

            Args:
                epsilon (float): Duration noise strength

            Returns:
                :class:`BitmapPHTrees.StableVolume`: The stable volume

            """
            return BitmapPHTrees.StableVolume(self, epsilon)

        def essential(self):
            """
            Returns:
                bool: True if the death time is infinity.
            """
            return self.dic["death-time"] is None

        def parent(self):
            """
            Returns:
                BitmapPHTrees.Node: The parent node of the node in the PH tree.
            """
            parent_id = self.dic["parent"]
            return BitmapPHTrees.Node(self.mt, self.mt.treedict["nodes"][parent_id])

        def isroot(self):
            """
            Returns:
               bool: True if the node is a root node.
            """
            return self.dic["parent"] is None

        def children(self):
            """
            Returns:
                list of :class:`BitmapPHTrees.Node`: All children nodes.
            """
            return [self.mt.node(child_id) for child_id in self.dic["children"] if not self.mt.is_trivial_id(child_id)]

        def __eq__(self, other):
            return (self.mt == other.mt) and (self.dic["id"] == other.dic["id"])

        def __repr__(self):
            return "BitmapPHTrees.Node({}, {})".format(self.birth_time(), self.death_time())

    class StableVolume(Volume):
        """
        This class represents a stable volume in :class:`BitmapPHTrees`.
        """

        def __init__(self, node, epsilon):
            self.node = node

            self._volume = set(tuple(p) for p in node.dic["volume"])
            for child_id in node.dic["children"]:
                child_dic = node.mt.treedict["nodes"][child_id]
                if self.is_unstable_child(child_dic, epsilon):
                    self._volume.difference_update(tuple(p) for p in child_dic["volume"])

        def is_unstable_child(self, child_dic, epsilon):
            is_sublevel = not self.node.mt.is_superlevel
            is_lower = self.node.mt.degree() == 0
            if is_lower and is_sublevel:
                return child_dic["death-time"] > self.node.death_time() - epsilon
            elif is_lower and not is_sublevel:
                return child_dic["death-time"] < self.node.death_time() + epsilon
            elif not is_lower and is_sublevel:
                return child_dic["birth-time"] < self.node.birth_time() + epsilon
            elif not is_lower and not is_sublevel:
                return child_dic["birth-time"] > self.node.birth_time() - epsilon

        def volume(self):
            """
            Returns the pixels of the stable volume.

            Returns:
                list[tuple[int,...]]: The coordinates of all pixels.
            """
            return list(self._volume)

    @staticmethod
    def to_paraview_node_from_nodes(nodes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode`
        object to visulize node volumes of the nodes.

        Args:
            nodes (list of :class:`BitmapPHTrees.Node`):
                The list of nodes to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.VTK: Paraview Pipeline node object.
        """
        all_volume = []
        for node in nodes:
            all_volume.extend(node.volume())

        min, max = bm.volume_range(all_volume)
        bitmap = bm.volume_to_bitmap(all_volume, (min, max))

        return pv_interface.VoxelData(bitmap, gui_name, min).threshold("value", (0.5, 1.0))

    to_pvnode_from_nodes = to_paraview_node_from_nodes
