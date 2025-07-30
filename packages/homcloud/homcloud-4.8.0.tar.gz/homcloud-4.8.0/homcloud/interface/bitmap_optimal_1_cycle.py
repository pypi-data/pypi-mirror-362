import homcloud.pict.optimal_one_cycle as pict_opt1cyc
import homcloud.paraview_interface as pv_interface
import homcloud.plotly_3d as p3d


class BitmapOptimal1Cycle(object):
    """The class represents an optimal (not volume-optimal) 1-cycle for bitmap.

    Computing volume-optimal cycle is very expensive for 3-D and
    higher dimensional cubical filtration. To fight against such
    a huge filtration, :meth:`Pair.optimal_1_cycle` is available.
    This method returns an instance of this class.
    """

    def __init__(self, orig):
        self.orig = orig

    def birth_time(self):
        """
        Returns:
            float: The birth time.
        """
        return self.orig.birth_time

    def death_time(self):
        """
        Returns:
            float: The death time.
        """
        return self.orig.death_time

    def birth_position(self):
        """
        Returns:
            tuple of float*N: The coordinate of birth position. (N: dimension)
        """
        return self.orig.path[0]

    def path(self):
        """
        Returns the path (loop) of the optimal 1-cycle.

        The first item and the last item is the same as :meth:`birth_position`.

        Returns:
            list of coord: The list of vertices of the loop ordered by the path
        """
        return self.orig.path

    def boundary_points(self):
        """
        Returns:
            list of coord: The list of vertices in the loop. Any vertex
                in the list is unique.
        """
        return self.orig.boundary_points()

    def to_paraview_node(self, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize an optimal 1-cycle.

        You can show the optimal 1-cycle by
        :meth:`homcloud.paraview_interface.show`. You can also
        adjust the visual by the methods of
        :class:`homcloud.paraview_interface.PipelineNode`.

        Args:
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        return self.to_paraview_node_for_1cycles([self], gui_name)

    @staticmethod
    def to_paraview_node_for_1cycles(cycles, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize multiple optimal 1-cycles.

        Args:
            cycles (list of :class:`Optimal1CycleForBitmap`):
                The optimal 1-cycles to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """

        drawer = pict_opt1cyc.prepare_drawer_for_paraview(len(cycles))
        for i, cycle in enumerate(cycles):
            cycle.orig.draw(drawer, i, str(i))
        f = pv_interface.TempFile(".vtk")
        drawer.write(f)
        f.close()
        return pv_interface.VTK(f.name, gui_name, f).set_representation("Wireframe")

    to_pvnode = to_paraview_node
    to_pvnode_for_1cycle = to_paraview_node_for_1cycles

    def to_plotly3d_trace(self, color=None, name=""):
        """
        Constructs a plotly's trace object to visualize the optimal 1-cycle

        Args:
            color (string or None): The name of the color
            name (string): The name of the object

        Returns:
            plotly.graph_objects.Mesh3d: Plotly's trace object
        """
        return p3d.Voxels(self.path(), color, name)

    to_plotly3d = to_plotly3d_trace

    def to_pyvista_mesh(self):
        """
        Constructs a PyVista's mesh object to visualize the optimal 1-cycle

        Returns:
            pyvista.PolyData: PyVista's mesh object
        """
        import homcloud.pyvistahelper as pvhelper

        return pvhelper.SparseVoxels(self.path())
