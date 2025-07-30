""" """

import subprocess
import warnings
import shutil
import sys
import enum
import operator
import os
import io

import numpy as np
from cached_property import cached_property

from homcloud.delegate import forwardable
import homcloud.alpha_filtration as alpha_filtration
import homcloud.rips as rips
import homcloud.bitmap
import homcloud.abstract_filtration as abstract_filtration
import homcloud.simplicial_levelset as simplicial_levelset
import homcloud.optvol as optvol
import homcloud.int_reduction as int_reduction
import homcloud.pdgm as pdgm
import homcloud.pdgm_format as pdgm_format
import homcloud.pict.optimal_one_cycle as pict_opt1cyc
import homcloud.optimal_one_cycle as opt1cyc
import homcloud.plot_PD_slice as plot_PD_slice
import homcloud.graph_optimal_one_cycle as graph_opt1cyc
from homcloud.spatial_searcher import SpatialSearcher

from .distance_transform import distance_transform
from .histogram import HistoSpec, SliceHistogram
from .optimal_volume import OptimalVolume, StableVolume
from .exceptions import VolumeNotFound
from .bitmap_optimal_1_cycle import BitmapOptimal1Cycle
from .boundary_map_optimal_1_cycle import Optimal1Cycle
from .graph_optimal_1_cycle import GraphOptimal1Cycle
from .ph0_component import PH0Components


class PDList(object):
    """Collection of 0th,1st,..,and q-th persitence diagrams.

    In HomCloud, diagrams for all degrees coming from a filtration
    are combined into a single file. This class is the interface to
    the file.

    Args:
       file (string or file): The pathname to a diagram file
       type (enum PDList.FileType): Type of diagram file. One of the following:
           idiagram, pdgm, or None (autodetected)
       cache (bool): Ignored (for backward compatibility)
       negate (bool): Ignored (for backward compatibility)
    """

    def __init__(self, file, filetype=None, cache=False, negate=False):
        if isinstance(file, str):
            self.path = file
            self.reader = pdgm_format.PDGMReader.open(file)
        else:
            self.path = getattr(file, "name", None)
            self.reader = pdgm_format.PDGMReader(file, self.path)

        PDList.assert_not_idiagram(filetype, self.path)

    def __repr__(self):
        return "PDList(path=%s)" % self.path

    def close(self):
        """
        Dispose PDList object and release resources.
        """
        self.reader.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @enum.unique
    class FileType(enum.Enum):
        IDIAGRAM = "idipha"
        PDGM = "pdgm"

    @property
    def pdgm_id(self):
        return self.reader.pdgm_id

    @staticmethod
    def compute_pd(filtration, save_to, parallels, algorithm, save_suppl_info):
        f = PDList.open_pdgm_file(save_to)
        filtration.compute_pdgm(f, algorithm, save_suppl_info)
        f.seek(0)
        return PDList(f, PDList.FileType.PDGM)

    @staticmethod
    def open_pdgm_file(save_to):
        if save_to is None:
            return io.BytesIO()
        else:
            return open(save_to, "w+b")

    @staticmethod
    def from_alpha_filtration(
        pointcloud,
        weight=False,
        no_squared=None,
        *,
        squared=None,
        subsets=False,
        check_acyclicity=False,
        algorithm=None,
        parallels=1,
        vertex_symbols=None,
        save_to=None,
        indexed=True,
        save_suppl_info=True,
        save_boundary_map=False,
        periodicity=None,
        save_phtrees=False,
        output_filetype=None,
    ):
        """Compute PDList by using an alpha filtration from a point cloud.

        Args:
            pointcloud (numpy.ndarray): Point cloud data. Each row
                represents a single point.
                Only 2D or 3D pointclouds are available.
            weight (bool): If False, the pointcloud has no weight. If True,
                the last column of the pointcloud ndarray is regarded as
                weights. Please note that the weight paramters of points
                should be the square of their own radii.
            squared (bool): By default, all birth/death times are squared.
                If squared is False, all computed birth/death times are
                not squared.
            no_squared (bool): See `squared` parameter.
            subsets (list[int] or bool or None):
                This parameter is used to introduce equivalence relationship.

                This parameter allows you to analyze the interspace structures
                between two or more objects in your pointcloud.

                If the grouped sub-pointcloud constructs a contractible subcomplex,
                the relative homology is comptuted.
                If the grouped sub-pointcloud constructs a subcomplexes whose connected components
                are contractible, each connected component in the subcomplexes
                is shrinked into a single point and
                birth-death pairs corresponding to the connected components are removed from the 0th PD.
                In the homcloud's code, minus infinity is assigned to the levels of
                all simplices in the subcomplex and PDs are comptuted, and all birth-death pairs whose
                birth time is -inf are removed from the diagrams.

                If `subsets` is None, normal persistent homology is computed.

                If `subsets` is a list of integers whose length is the same
                as the number of points, the points are grouped
                by the integers and the gaps in the points in the same
                group is filled. The integer -1 in this list means
                that the point does not belong to any group.

                If subsets is True, the last column of `pointcloud` is regarded
                as the list of group id.
            check_acyclicity (bool):
                Checks the acyclicity of each grouped points in subsets
                if True. This parameter is used only if `subsets` parameter
                is used.
            algorithm (string or None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                ``homcloud.interface.PDList(FILE_PATH)``.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_suppl_info (bool): Various supplimentary information is saved to
                the file `save_to`. The default is True. This information is
                required to show birth and death pixels and optimal volumes.
                If you do not use such HomCloud's functionality and you want to
                reduce the size of the file, please set the argument ``False``.
                If False, only birth and death times are stored to the file.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.
            periodicity (tuple[tuple[float, float], tuple[float, float]], tuple[tuple[float, float], tuple[float, float], tuple[float, float]] or None):
                Periodic boundary condition. Peridic boundary condition is not available for 2D alpha shape.
            save_phtrees (bool): The PH-trees for (n-1)st PH is saved if True.
                Use meth:`PD.load_phtrees` to load the PH trees.
        Returns:
            The :class:`PDList` object computed from the pointcloud.

        Warn:
            The pointcloud should be general position; that is, all combinations of three points should not be on a signle line, all combinations of four points should not be on a signle plane for 3D, all combinations of four points should not be on a single circle, and all combinations of five points should not be on a single sphere for 3D. If the input data does not satisfy general position condition, the alpha filtration cannot be computed correctly.
            If you want to use peridic boundary condition, the pointcloud has sufficiently many points. If the number of points is small, alpha shape cannot be computed correctly.


        Examples:
            >>> import homcloud.interface as hc
            >>> pointcloud = hc.example_data("tetrahedron")
            >>> hc.PDList.from_alpha_filtration(pointcloud)
            -> Returns a new PDList
        """
        assert indexed
        assert (save_phtrees and save_boundary_map) or (not save_phtrees)
        PDList.assert_not_idiagram(output_filetype, save_to)

        def squared_parameter():
            if squared is not None:
                return squared
            if no_squared is not None:
                return not no_squared
            return True

        squared = squared_parameter()

        pointcloud = pointcloud.astype(float)
        num_points = pointcloud.shape[0]
        dim = pointcloud.shape[1] - int(weight is True) - int(subsets is True)

        if isinstance(weight, np.ndarray):
            pointcloud = np.hstack([pointcloud, weight.reshape(num_points, 1)])
            weight = True

        if isinstance(subsets, np.ndarray):
            pointcloud = np.hstack([pointcloud, subsets.reshape(num_points, 1)])
            subsets = True

        alpha_shape = alpha_filtration.AlphaShape.build(pointcloud, dim, weight, subsets, periodicity)

        if check_acyclicity:
            alpha_shape.check_subsets_acyclicity()
        if subsets:
            alpha_shape.become_partial_shape()

        filtration = alpha_shape.create_filtration(squared, vertex_symbols, save_boundary_map, save_phtrees)

        return PDList.compute_pd(filtration, save_to, parallels, algorithm, save_suppl_info)

    @staticmethod
    def from_bitmap_levelset(
        array,
        mode="sublevel",
        type="bitmap",
        algorithm=None,
        parallels=1,
        periodicity=None,
        save_to=None,
        indexed=True,
        save_suppl_info=True,
        save_boundary_map=False,
        output_filetype=None,
    ):
        """
        Computes superlevel/sublevel PDList from an n-dimensional bitmap.

        Args:
            array (numpy.ndarray): An n-dimensional array.
            mode (string): The direction of the filtration.
               "superlevel" or "sublevel".
            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical" and the computation for "bitmap" is
               faster than "cubical".
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "homccubes-0", "homccubes-1", "homccubes-2"
                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            periodicity (None, list of bool):
                The list of booleans to specify the periodicity.
                For example, if your array is 2D and you want to make
                the array periodic only in 0-axis, you should give `[True, False]`.
                Any periodic structure is not used if None.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            indexed (bool): Always must be True.
            save_suppl_info (bool): Various supplimentary information is saved to
                the file `save_to`. The default is True. This information is
                required to show birth and death pixels and optimal_1_cycles.
                If you do not use such HomCloud's functionality and you want to
                reduce the size of the file, please set the argument ``False``.
                If False, only birth and death times are stored to the file.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles. This parameter is only available
                if the type is "cubical".

        Returns:
            The :class:`PDList` object computed from the bitmap.

        Examples:
            >>> import numpy as np
            >>> import homcloud.interface as hc
            >>> bitmap = np.array([[1.5, 2.0, 0.5],
            >>>                    [0.8, 4.1, 0.9],
            >>>                    [1.3, 1.8, 1.3]])
            >>> hc.PDList.from_bitmap_levelset(bitmap, "sublevel")
            -> Returns PDList object for sublevel persistence diagrams
            >>> hc.PDList.from_bitmap_levelset(bitmap, "superlevel",
            >>>                             periodicity=[True, True])
            -> Returns PDList object for superlevel PDList on a 2-torus
        """
        assert indexed
        PDList.assert_not_idiagram(output_filetype, save_to)

        array = array.astype(float, copy=False)
        if mode == "sublevel":
            flip_sign = False
        elif mode == "superlevel":
            array = -array
            flip_sign = True
        else:
            raise ValueError("unknown mode: {}".format(mode))

        bitmap = homcloud.bitmap.Bitmap(array, flip_sign, periodicity, save_boundary_map)
        if type == "cubical":
            filt = bitmap.build_cubical_filtration()
        else:
            filt = bitmap.build_bitmap_filtration()

        return PDList.compute_pd(filt, save_to, parallels, algorithm, save_suppl_info)

    @staticmethod
    def from_bitmap_distance_function(
        binary_pict,
        signed=False,
        metric="manhattan",
        type="bitmap",
        mask=None,
        algorithm=None,
        parallels=1,
        save_to=None,
        indexed=True,
        save_suppl_info=True,
        save_boundary_map=False,
        output_filetype=None,
    ):
        """
        This method is obsolete. Please use the combination of
        :meth:`PDList.from_bitmap_levelset` and
        :meth:`distance_transform` instead.

        Computes erosion/dilation PDList from an n-dimensional bitmap.

        In other words, this method computes the sublevel filtration
        whose level function is the distance function.

        Args:
            binary_pict (numpy.ndarray): An n-dimensional boolean array.
            signed (bool): The signed distance function is used
               instead of the normal distance function if True.
            metric (string): The metric. One of the followings:

               * "manhattan"
               * "chebyshev"
               * "euclidean"

            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical". However, if you want to use the following
               functionality, you must use "cubical" format.

               * optimal volume/volume optimal cycle
               * dependency check for a field

            mask (numpy.ndarray or None): The mask bitmap.
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "homccubes-0", "homccubes-1", "homccubes-2"
                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.

        Returns:
            The :class:`PDList` object computed from the bitmap.

        """
        warnings.warn(
            "interface.PDList.from_bitmap_distance_function is obsolete."
            "Please use interaface.distance_transform and BitmapPHTreesPair.",
            PendingDeprecationWarning,
        )
        assert output_filetype is None
        return PDList.from_bitmap_levelset(
            distance_transform(binary_pict, signed, metric, None, mask),
            "sublevel",
            type,
            algorithm,
            parallels,
            None,
            save_to,
            indexed,
            save_suppl_info,
            save_boundary_map,
            output_filetype,
        )

    @staticmethod
    def from_rips_filtration(
        distance_matrix,
        maxdim,
        maxvalue=np.inf,
        simplicial=False,
        vertex_symbols=None,
        algorithm=None,
        parallels=1,
        save_boundary_map=False,
        save_graph=False,
        save_cocycles=False,
        save_to=None,
    ):
        """
        Compute a PDList from a distance matrix by using Vietoris-Rips
        filtrations.

        Args:
            distance_matrix (numpy.ndarary): KxK distance matrix.
                When you use "ripser" as the algorithm, the datatype of the matrix is converted into float32 internally
                since Ripser only supports float32.
            maxdim (int): Maximal homology degree computed.
            maxvalue (float): Maximal distance for constructing a filtration.
                All longer edges do not apper in the constructed filtration.
            simplicial (bool): If True, construct a simplicial complex for
                :meth:`Pair.optimal_volume` (slow)
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            algorithm: The name of the algorithm. An appropriate algorithm is
                automatically selected if None is given.
                The default is "ripser" for the normal case with `simplicial=False`.

                If simplicial is False, "dipha" and "ripser" are available.
                If simpliclal is True, "dipha", "phat-twist", "phat-chunk-parallel"
                are availbale.

            paralles: The number of threads for computation. This value is
                used only if algorith is "dipha".
            save_boundary_map (bool):
                The boundary map constructed by the given distance matrix is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles. This option is only available
                if `simplicial` is True.
            save_graph (bool):
                The graph structure of rips filtration is saved in .pdgm file.
            save_to (string or None): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.

        Returns:
            The :class:`PDList` object computed from the distance matrix.

        """
        assert not (simplicial and save_graph)
        dm = rips.DistanceMatrix(distance_matrix, maxdim, maxvalue, vertex_symbols)
        if simplicial:
            filtration = dm.build_simplicial_filtration(save_boundary_map)
        else:
            filtration = dm.build_rips_filtration(save_graph, save_cocycles)

        return PDList.compute_pd(filtration, save_to, parallels, algorithm, True)

    @staticmethod
    def from_simplicial_levelset(
        simplicial_function,
        vertex_symbols=None,
        algorithm=None,
        save_to=None,
        save_boundary_map=False,
        save_suppl_info=True,
    ):
        """
        Compute a PDList from a simplicial level function.

        Args:
            simplicial_function: (dict[simplex, float]): the level of each simplex.
            vertex_symbols (Option[list[str]]): The names of all vertices.
            algorithm (Option[str]): The name of the algorithm.
            save_to (Option[str]): The file path which the computation result is
                saved into.
            save_boundary_map (bool):
                The boundary map is saved if this parameter is True.
                The boundary map is used to compute volume optimal cycles.

        Returns:
            :class:`PDList`: The PDList computed from the boundary map.

        Examples:
            >>> import homcloud.interface as hc
            >>>
            >>> pdlist = hc.PDList.from_simplicial_levelset(
            >>>     {
            >>>         (0,): 1.0,
            >>>         (1,): 1.1,
            >>>         (2,): 1.1,
            >>>         (0, 1): 1.1,
            >>>         (1, 2): 1.1,
            >>>         (3,): 1.2,
            >>>         (2, 3): 1.2,
            >>>         (0, 3): 1.3,
            >>>         (1, 3): 1.4,
            >>>         (0, 1, 3): 1.5,
            >>>     },
            >>>     vertex_symbols=["a", "b", "c", "d"],
            >>>     save_boundary_map=True,
            >>> )
            >>> pd1 = pdlist[1]
            >>> pd1.births
            [1.4]
            >>> pd1.deaths
            [1.5]
            >>> pd1.essential_births
            [1.3]
        """
        filtration = simplicial_levelset.SimplicialFiltration(simplicial_function, vertex_symbols, save_boundary_map)
        return PDList.compute_pd(filtration, save_to, 1, algorithm, save_suppl_info)

    @staticmethod
    def from_boundary_information(
        boundary, levels, symbols=None, algorithm=None, parallels=1, save_to=None, save_boundary_map=False
    ):
        """
        Compute a PDList from a boundary map and level information
        for abstract combinatorial complex.

        Args:
            boundary (list of (int, list of int, list of int)):
                list of cells and their boundary information. (dim of cell, list of indices of, list of coefs)
            levels (numpy.ndarray): level of each cell. **Cells should be ordered in level-increasing order**.
            symbols (list of string, None): The names of each cell.
            algorithm (string, nil): The name of the algorithm.
                An appropriate algorithm is automatically selected if None is given.
            save_to (string or None): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map is saved if this parameter is True.
                The boundary map is used to compute volume optimal cycles.

        Returns:
            :class:`PDList`: The PDList computed from the boundary map.

        Examples:
            >>> import homcloud.interface as hc
            >>>
            >>> hc.PDList.from_boundary_information([
            >>>     [0, [], []], [0, [], []], [0, [], []],  # theee 0-simplices
            >>>     [1, [0, 1], [1, -1]], [1, [1, 2], [1, -1]], [1, [0, 2], [1, -1]],  # three 1-simplices
            >>>     [2, [3, 4, 5], [1, 1, -1]],  # a 2-simplex
            >>> ], [
            >>>     -0.02, 0.01, 0.01,  # levels of 0-simplices
            >>>     0.1, 0.2, 0.3,  # levels of 1-simplices
            >>>     0.6  # level of the 2-simplex
            >>> ], save_to="pd.pdgm"
            >>> )
            >>> pd1 = hc.PDList("pd.pdgm").dth_diagram(1)
            >>> print(pd1.births)  # => [0.3]
            >>> print(pd1.deaths)  # => [0.6]
        """
        assert len(boundary) == len(levels)
        assert symbols is None or len(symbols) == len(boundary)
        for k in range(len(levels) - 1):
            assert levels[k] <= levels[k + 1]

        maxdim = 0
        for column in boundary:
            maxdim = max(maxdim, column[0])
        if symbols is None:
            symbols = [str(n) for n in range(len(levels))]

        filtration = abstract_filtration.AbstractFiltration(boundary, maxdim, levels, symbols, save_boundary_map)

        return PDList.compute_pd(filtration, save_to, 1, algorithm, True)

    def save(self, dest):
        """Save the PDList into `dest`.

        Args:
            dest (string): The filepath which the diagram data is saved into.
        """
        with open(dest, "wb") as destfile:
            srcfile = self.reader.infile
            srcfile.seek(0)
            shutil.copyfileobj(srcfile, destfile)

    def dth_diagram(self, d, load_indexed_pairs=True):
        """Return `d`-th persistence diagram from PDList.

        Args:
            d (int): the degree of the diagram
            load_indexed_pairs (bool): index information is loaded if True.
                Otherwise, the information is not loaded. This parameter will
                be helpful to reduce the loading time.
        Returns:
            The :class:`PD` object.

        """
        return PD(self.path, pdgm.PDGM(self.reader, d, load_indexed_pairs))

    __getitem__ = dth_diagram

    def invoke_gui_plotter(
        self,
        d,
        x_range=None,
        xbins=None,
        y_range=None,
        ybins=None,
        colorbar={"type": "linear"},
        title=None,
        unit_name=None,
        aspect="equal",
        optimal_volume=False,
        optimal_volume_options=None,
    ):
        """Invoke the GUI plotter.

        Args:
            d (int): The degree of the PD.
        """

        def format_range(r):
            return "[{}:{}]".format(r[0], r[1])

        options = ["-d", str(d)]
        if x_range:
            options.extend(["-x", format_range(x_range)])
        if xbins:
            options.extend(["-X", str(xbins)])
        if y_range:
            options.extend(["-y", format_range(y_range)])
        if ybins:
            options.extend(["-Y", str(ybins)])
        if colorbar["type"] == "linear":
            pass
        elif colorbar["type"] == "log":
            options.append("-l")
        elif colorbar["type"] == "loglog":
            options.append("--loglog")
        if "max" in colorbar:
            options.extend(["--vmax", str(colorbar["max"])])
        if title is not None:
            options.extend(["--title", str(title)])
        if unit_name is not None:
            options.extend(["--unit-name", str(unit_name)])
        options.extend(["--aspect", aspect])
        if optimal_volume:
            options.extend(["--optimal-volume", "on"])
        subprocess.Popen([sys.executable, "-m", "homcloud.plot_PD_gui"] + options + [self.path])

    def bitmap_phtrees(self, degree):
        """
        Read a :class:`BitmapPHTrees` object computed by
        :meth:`BitmapPHTrees.for_bitmap_levelset`.

        Args:
           degree (int): The PD degree. 0 or (n-1).

        Returns:
           A :class:`BitmapPHTrees` object
        """
        from .bitmap_phtrees import BitmapPHTrees

        treedict = self.reader.load_simple_chunk("bitmap_phtrees", degree)
        return BitmapPHTrees(treedict, self.reader.metadata["sign_flipped"])

    def check_coefficient_problem(self):
        pdgm = self.dth_diagram(0).pd
        checker = int_reduction.build_checker(pdgm.input_dim, pdgm.boundary_map_chunk)
        return checker.check()

    @staticmethod
    def assert_not_idiagram(output_filetype, path):
        assert_message = "idiagram format is not available after 3.0"
        assert output_filetype != PDList.FileType.IDIAGRAM, assert_message
        if path is not None:
            assert os.path.splitext(path)[1] != ".idiagram", assert_message


#: Obsolete, for backward compatibility
PDs = PDList


@forwardable
class PD(object):
    """
    The class for a single persistence diagram.

    You can get the object of this class by :meth:`PDList.dth_diagram` or
    :meth:`PDList.__getitem__`.

    Attributes:
        path (str): File path
        degree (int): Degree of the PD
        births (numpy.ndarray[num_of_pairs]): Birth times
        deaths (numpy.ndarray[num_of_pairs]): Death times
        birth_positions: Birth positions for birth-death pairs
        death_positions: Death positions for birth-death pairs
        essential_births (numpy.ndarray[num_of_ess_pairs]):
            Birth times of essential birth-death pairs (birth-death pairs with
            infinite death time)
        essential_birth_positions:
            Birth positions for essential birth-death pairs
    """

    def __init__(self, path, pd):
        self.path = path
        self.pd = pd

    __delegator_definitions__ = {
        "pd": [
            "degree",
            "births",
            "deaths",
            "birth_positions",
            "death_positions",
            "essential_births",
            "essential_birth_positions",
            "sign_flipped",
            "filtration_type",
            "alpha_weighted",
            "alpha_radii_squared",
            "get_geometry_resolver",
        ]
    }

    def __repr__(self):
        return "PD(path=%s, d=%d)" % (self.path, self.pd.degree)

    @property
    def pdgm_id(self):
        return self.pd.pdgm_id

    def birth_death_times(self):
        """
        Returns the  birth times and death times.

        Returns:
            tuple[numpy.ndarray, numpy.ndarray]:
                The pair of birth times and death times
        """
        return self.pd.births, self.pd.deaths

    def histogram(
        self,
        x_range=None,
        x_bins=128,
        y_range=None,
        y_bins=None,
    ):
        """
        Returns the histogram of the PD.

        This is the shortcut method of :meth:`HistoSpec.pd_histogram`

        Args:
           x_range (tuple[float, float] or None): The lower and upper range
               of the bins on x-axis. If None is given, the range
               is determined from the minimum and maximum of
               the birth times and death times of all pairs.
           y_range (int): The number of bins on x-axis.
           y_range (tuple[float, float] or None): The lower and upper range
               of the bins on y-axis. Same as `x_range` if None is given.
           y_bins (int or None): The number of bins on y-axis.
               Same as `x_bins` if None is given.

        Returns:
            The :class:`Histogram` object.
        """
        return HistoSpec(x_range, x_bins, y_range, y_bins, self.pd).pd_histogram(self.pd)

    def load_phtrees(self):
        """
        Load a PH trees from the diagram.

        This method is available only for the (n-1)th diagram of an alpha filtration
        of n-dimensional pointcloud.

        You should compute the PH trees by :meth:`PDList.from_alpha_filtration`
        with ``save_phtrees=True`` before using this method.

        Returns:
            The :class:`PHTrees` object of the (n-1)th PH.
        """
        from .phtrees import PHTrees

        if self.degree != self.pd.input_dim - 1:
            raise (ValueError("The degree of PD must be the same as dim - 1 when PHTrees is used."))
        if self.pd.pdgmreader.load_simple_chunk("phtrees") is None:
            raise (
                ValueError("phtrees must be saved (save_phtrees=True) when PDs are computed before PHTrees is used.")
            )

        return PHTrees.from_pdgm(self.pd)

    def pair(self, nth):
        """Returns `nth` birth-death pairs.

        Args:
            nth (int): Index of the pair.

        Returns:
            :class:`Pair`: The nth pair.
        """
        return Pair(self, nth)

    def pairs(self):
        """Returns all pairs of the PD.

        Returns:
            list of :class:`Pair`: All birth-death pairs.
        """
        return [self.pair(n) for n in range(self.pd.num_pairs)]

    def nearest_pair_to(self, x, y):
        """Returns a pair closest to `(x, y)`.

        Args:
            x (float): X (birth) coordinate.
            y (float): Y (death) coordinate.

        Returns:
            :class:`Pair`: The cleosest pair.
        """
        return self.spatial_searcher.nearest_pair(x, y)

    @cached_property
    def spatial_searcher(self):
        return SpatialSearcher(self.pairs(), self.births, self.deaths)

    def pairs_in_rectangle(self, xmin, xmax, ymin, ymax):
        """Returns all pairs in the rectangle.

        Returns all birth-death pairs whose birth time is in
        the interval `[xmin, xmax]` and
        whose death time is in `[ymin, ymax]`.

        Args:
           xmin (float): The lower range of birth time.
           xmax (float): The upper range of birth time.
           ymin (float): The lower range of death time.
           ymax (float): The upper range of death time.

        Returns:
           list of :class:`Pair`: All birth-death pairs in the rectangle.
        """
        return self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)

    @staticmethod
    def empty():
        """Returns a persistence diagram which has no birth-death pairs.

        Returns:
            PD: A PD object with no birth-death pair.
        """
        return PD(None, pdgm.empty_pd())

    @staticmethod
    def from_birth_death(degree, births, deaths, ess_births=np.array([]), sign_flipped=False):
        """Returns a persistence diagram which birth and death times are given lists.

        Args:
            degree (int): The degree of the returned diagram
            births (numpy.ndarray): The birth times
            deaths (numpy.ndarray): The death times
            ess_births (numpy.ndarray): The birth times of essential pairs
            sign_flipped (bool): The sign is flipped if True
        Returns:
            PD: A PD object
        """
        return PD(None, pdgm.SimplePDGM(degree, births, deaths, ess_births, sign_flipped))

    def slice_histogram(self, x1, y1, x2, y2, width, bins=100):
        """Returns 1D histogram of birth-death pairs in a thin strip.

        This method computes a 1D hitogram of birth-death pairs
        in the thin strip whose center line is
        `(x1, y1) - (x2, y2)` and whose width is `width`.

        Args:
            x1 (float): The x(birth)-coordinate of the starting point.
            y1 (float): The y(death)-coordinate of the starting point.
            x2 (float): The x(birth)-coordinate of the ending point.
            y2 (float): The y(death)-coordinate of the ending point.
            width (float): Width of the strip.
            bins (int): The number of bins.

        Returns:
            :class:`SliceHistogram`: The histogram.
        """
        transl, mat = plot_PD_slice.transform_to_x_axis(np.array([x1, y1]), np.array([x2, y2]))
        xy = np.dot(mat, np.array([self.births, self.deaths]) - transl.reshape(2, 1))
        mask = (xy[0, :] >= 0) & (xy[0, :] <= 1) & (np.abs(xy[1, :]) < width / 2)
        values, edges = np.histogram(xy[0, mask], bins, (0, 1))
        return SliceHistogram(values, edges, x1, y1, x2, y2)

    def optvol_optimizer_builder(self, cutoff_radius, num_retry, lp_solver):
        if self.pd.boundary_map_chunk is None:
            raise (
                ValueError(
                    'Optimal/Stable volume requires boundary_map: "save_boundary_map=True"'
                    " is requried when a PD is computed."
                )
            )

        if cutoff_radius is None:
            return optvol.OptimizerBuilder(self.degree, self.pd.boundary_map_chunk, lp_solver)
        else:
            if self.filtration_type == "alpha":
                return optvol.OptimizerBuilder.from_alpha_pdgm(self.pd, cutoff_radius, num_retry, lp_solver)
            elif self.filtration_type == "cubical":
                return optvol.OptimizerBuilder.from_cubical_pdgm(self.pd, cutoff_radius, num_retry, lp_solver)
            else:
                raise ValueError("cutoff is not available for {}".format(self.filtration_type))

    def torch_tensor_births_deaths(self, torch_input):
        if self.filtration_type == "bitmap":
            return self.torch_tensor_births_deaths_bitmap(torch_input)
        if self.filtration_type == "alpha":
            return self.torch_tensor_births_deaths_alpha(torch_input)
        raise ValueError("Now torch_tensor_births_deaths supports only bitmap or alpha filtrations")

    def torch_tensor_births_deaths_bitmap(self, torch_bitmap):
        births = torch_bitmap[np.array(self.birth_positions, dtype=int).transpose().tolist()]
        deaths = torch_bitmap[np.array(self.death_positions, dtype=int).transpose().tolist()]
        return births, deaths

    def torch_tensor_births_deaths_alpha(self, torch_pointcloud):
        import torch
        import homcloud.geometry.torch_utils as torch_utils

        def circumradius(simplex):
            if len(simplex) == 1:
                return torch.tensor(0.0)

            torch_simplex = torch_pointcloud[simplex]

            if len(simplex) == 2:
                return torch_utils.edge_squared_circumradius(torch_simplex)
            if len(simplex) == 3:
                if self.pd.input_dim == 2:
                    return torch_utils.triangle_squared_circumradius_2d(torch_simplex)
                if self.pd.input_dim == 3:
                    return torch_utils.triangle_squared_circumradius_3d(torch_simplex)
            if len(simplex) == 4:
                return torch_utils.tetrahedron_squared_circumradius_3d(torch_simplex)

        assert not self.alpha_weighted, "weighted alpha filtration is not supported"
        assert self.alpha_radii_squared, "non-squared alpha filtration is not supported"

        index_to_simplex = self.pd.alpha_coord_resolver.index_to_simplex

        births = torch.hstack([circumradius(index_to_simplex[index]) for index in self.pd.birth_indices])
        deaths = torch.hstack([circumradius(index_to_simplex[index]) for index in self.pd.death_indices])
        return births, deaths


class Pair(object):
    """
    A class representing a birth-death pair.

    Attributes:
        diagram (:class:`PD`): The diagram which the birth-death pair
            belongs to.
    """

    def __init__(self, diagram, nth):
        self.diagram = diagram
        self.nth = nth

    def __iter__(self):
        return (self.birth_time(), self.death_time()).__iter__()

    def birth_time(self):
        """Returns the birth time of the pair.

        Returns:
            float: The birth time
        """
        return self.diagram.births[self.nth]

    def death_time(self):
        """Returns the death time of the pair.

        Returns:
            float: The death time
        """
        return self.diagram.deaths[self.nth]

    #: float: The birth time
    birth = property(birth_time)
    #: float: The death time
    death = property(death_time)

    @property
    def birth_position(self):
        """Birth position for the birth-death pair"""
        return self.diagram.birth_positions[self.nth]

    birth_pos = property(operator.attrgetter("birth_position"))
    """ Alias of :attr:`birth_position` """

    @property
    def death_position(self):
        """Death position for the birth-death pair"""
        return self.diagram.death_positions[self.nth]

    death_pos = property(operator.attrgetter("death_position"))
    """ Alias of :attr:`death_position` """

    @property
    def birth_index(self):
        return self.diagram.pd.birth_indices[self.nth]

    @property
    def death_index(self):
        return self.diagram.pd.death_indices[self.nth]

    @property
    def birth_position_symbols(self):
        """list of string: Birth simplex for the birth-death pair by symbols. Only available for alpha filtrations."""
        return self.diagram.pd.alpha_symbol_resolver.resolve_cell(self.birth_index)

    @property
    def death_position_symbols(self):
        """list of string: Death simplex for the birth-death pair by symbols. Only available for alpha filtrations."""
        return self.diagram.pd.alpha_symbol_resolver.resolve_cell(self.death_index)

    def optimal_volume(
        self,
        cutoff_radius=None,
        solver=None,
        solver_options={},
        constrain_birth=False,
        num_retry=4,
        integer_programming=False,
    ):
        """Return the optimal volume of the pair.

        See the paper by `Obayashi (2018) <https://doi.org/10.1137/17M1159439>`_
        if you want to know more about optimal volumes.

        It is possible to get better results with stable volumes than with optimal volumes.
        See :meth:`stable_volume` for the details of stable volumes.

        Args:
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            solver_options (dict[str, Any]): Options for LP sovlers.
                The options are forwarded to Pulp program.
            constrain_birth (bool): Now this value is not used.
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Integer constrains are used if True.
                Integer constrains make the computation slower, but
                possibly you get a better result.

        Returns:
            :class:`OptimalVolume`: The optimal volume.

        Raises:
            VolumeNotFound: Raised if the volume is not fould.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        ovfinder = optvol.OptimalVolumeFinder(
            self.diagram.optvol_optimizer_builder(cutoff_radius, num_retry, lp_solver)
        )

        result = ovfinder.find(self.birth_index, self.death_index)
        self.check_optimal_volume_error(result)
        return OptimalVolume(self, result.cell_indices, result)

    def check_optimal_volume_error(self, result):
        if isinstance(result, optvol.Failure):
            result.pair = tuple(self)
            raise VolumeNotFound(result.status, result.message)

    def stable_volume(
        self,
        threshold,
        cutoff_radius=None,
        solver=None,
        solver_options={},
        constrain_birth=False,
        num_retry=4,
        integer_programming=False,
    ):
        """Returns the stable volume of the pair.

        See `Obayashi (2023) <https://doi.org/10.1007/s41468-023-00119-8>`_
        if you want to know more about optimal volumes.

        Args:
            threshold (float): The noise bandwidth.
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            solver_options (dict[str, Any]): Options for LP sovlers.
                The options are forwarded to Pulp program.
            constrain_birth (bool): Ignored
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Ignored.
        Returns:
            :class:`StableVolume`: The stable volume.
        """
        lp_solver = optvol.find_lp_solver(solver, solver_options)
        finder = optvol.TightenedVolumeFinder(
            self.diagram.optvol_optimizer_builder(cutoff_radius, num_retry, lp_solver),
            self.diagram.pd.index_to_level,
            threshold,
        )
        result = finder.find(self.birth_index, self.death_index)
        self.check_optimal_volume_error(result)
        return StableVolume(self, result.cell_indices, threshold, result)

    tightened_volume = stable_volume

    def optimal_1_cycle(self, weighted=False, torelance=None):
        """Returns the optimal (not volume-optimal) 1-cycle
        corresponding to the birth-death pair.

        You can calculate similar infomormation using :meth:`optimal_volume`, but optimal_volume
        optimal_volume may be expensive, especiall for Vietoris-Rips filtration.
        optimal_1_cycle can be computed at a lower cost than optimal_volume.
        In general, an optimal volume gives better information about the birth-death pair, and
        an optimal 1-cycle gives an approximation of the optimal volume.

        The algorithm in optimal_1_cycle computes the minimal loop that includes a birth edge
        (alpha, rips, abstract) or birth pixel (bitmap).

        This method is available only when degree == 1.

        If you want to compute optimal 1-cycle. You need to pass the following argument when computing
        persistence diagrams.

        * Vietoris-Rips filtration by :meth:`PDList.from_rips_filtration`: `save_graph=True`.
          In this case, this method returns an object of :class:`GraphOptimal1Cycle`.
        * Alpha filtration by :meth:`PDList.from_alpha_filtration`: `save_boundary_map=True`
          In this case, this method returns an object of :class:`Optimal1Cycle`.
        * Abstract filtration by :meth:`PDList.from_boundary_information`: `save_boundary_map=True`.
          In this case, this method returns an object of :class:`Optimal1Cycle`.
        * Bitmap filtration by :meth:`PDList.from_bitmap_levelset`: `save_suppl_info=True`
          In this case, this method returns an object of :class:`BitmapOptimal1Cycle`.

        Args:
            weighted (bool): Use graph weight to find shortest loop. Only available for Vietoris-Rips filtration
            torelance (None or float): Noise bandwidth parameter for Reconstructed Shortest Cycles.
              Only available for Vietoris-Rips filtration.
              See https://mtsch.github.io/Ripserer.jl/dev/generated/cocycles/#Reconstructed-Shortest-Cycles
              if you know more about Reconstructed shortest cycles.

        Returns:
            :class:`BitmapOptimal1Cycle` | :class:`GraphOptimal1Cycle` | :class:`Optimal1Cycle` : The optimal 1-cycle.

        Raises:
            AssertionError: Raised if the filtration is not a bitmap filtration
                or the degree of the pair is not 1.
        """
        assert self.degree == 1
        if self.diagram.pd.has_chunk("graph_weights"):
            return self.graph_optimal_1_cycle(weighted, torelance)
        elif self.diagram.filtration_type == "bitmap":
            return self.bitmap_optimal_1_cycle()
        else:
            return self.boundary_map_optimal_1_cycle()

    def bitmap_optimal_1_cycle(self):
        finder = pict_opt1cyc.Finder(self.diagram.pd)
        return BitmapOptimal1Cycle(finder.query_pair(self.birth_index, self.death_index))

    def boundary_map_optimal_1_cycle(self):
        return Optimal1Cycle(self, opt1cyc.search_on_chunk_bytes(self.diagram.pd.boundary_map_bytes, self.birth_index))

    def graph_optimal_1_cycle(self, weighted=False, torelance=None):
        if torelance is None:
            return GraphOptimal1Cycle(
                self, graph_opt1cyc.search(self.diagram.pd.graph_adjacent_matrix, self.birth_time(), weighted)
            )
        else:
            return GraphOptimal1Cycle(
                self,
                graph_opt1cyc.search_with_cocycle(
                    self.diagram.pd.graph_adjacent_matrix,
                    self.representative_cocycle(),
                    self.birth_time(),
                    torelance,
                    weighted,
                ),
            )

    def __eq__(self, other):
        return isinstance(other, Pair) and self.diagram == other.diagram and self.nth == other.nth

    def __repr__(self):
        return "Pair({}, {})".format(self.birth_time(), self.death_time())

    def lifetime(self):
        """The lifetime of the pair.

        Returns:
            float: The lifetime (death - birth) of the pair.
        """
        return self.death_time() - self.birth_time()

    def __hash__(self):
        return id(self.diagram) + (int(self.nth) << 20)

    def representative_cocycle(self):
        return self.diagram.pd.representative_cocycle(self.degree, self.nth)

    @property
    def degree(self):
        """The degree of the pair."""
        return self.diagram.degree

    def ph0_components(self, epsilon=0.0):
        assert self.diagram.filtration_type in ["alpha"]
        return PH0Components(self, epsilon)
