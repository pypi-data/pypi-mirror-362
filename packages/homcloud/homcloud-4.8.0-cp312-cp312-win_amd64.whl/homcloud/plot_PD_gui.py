import sys
import os
import argparse
import tempfile
import uuid
import shlex
import functools
import json

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QProgressDialog
from PyQt5.QtCore import QCoreApplication, Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon, QCursor, QPixmap
import numpy as np
import matplotlib

matplotlib.use("Qt5Agg")  # noqa
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from homcloud.plot_PD_gui_ui import Ui_MainWindow
from homcloud.plot_PD import (
    add_arguments_for_auxinfo,
    AuxPlotInfo,
    ZSpec,
    PDColorHistogramPlotter,
    PDContourPlotter,
)
from homcloud.argparse_common import add_arguments_for_load_diagrams, add_arguments_for_histogram_rulers, parse_bool
import homcloud.utils as utils
import homcloud.resources  # noqa
from homcloud.version import __version__
from homcloud.histogram import Ruler, PDHistogram
import homcloud.pdgm as pdgm


class MainWindow(QMainWindow):
    def __init__(self, pd, phtrees_resolver, tmpdir, args, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # initialize data
        self.pd = pd
        self.x_range = args.x_range or pd.minmax_of_birthdeath_time()
        self.y_range = args.y_range or self.x_range
        self.normalize_constant = args.normalize_constant
        self.aux_plot_info = AuxPlotInfo.from_args(args)

        # initialize event handlers for mouse events
        self.measure_distance_handler = MeasureDistanceHandler(self)
        self.rectangle_zoom_handler = RectangleZoomHandler(self)
        self.count_pairs_handler = CountPairsHandler(self)
        self.phtrees_handler = PHTreesHandler.create(phtrees_resolver, tmpdir, self)
        self.phtrees_range_query_handler = PHTreesRangeQueryHandler.create(phtrees_resolver, tmpdir, self)
        self.optimal_volume_handler = OptimalCycleHandler.create(
            pd, self, tmpdir, args.optimal_volume, shlex.split(args.optimal_volume_options)
        )
        self.current_canvas_ev_handler = NoOpMouseHandler()

        # setup UI part2
        self.setWindowTitle(args.title)
        self.figure = self.canvas = None
        self.add_matplotlib_canvas()
        self.ui.actionMeasure.setIcon(QIcon(":ui/icon_measure.png"))
        self.ui.actionRange.setIcon(QIcon(":ui/icon_range.png"))
        if not self.phtrees_handler.is_available():
            self.invalidate_phtrees_widgets()
        if not self.optimal_volume_handler.is_available():
            self.invalidate_optimal_volume_widgets()

        self.store_initial_widget_values(args)

        self.ax = self.background = None
        self.replot_history = []

        self.connect_signals()

        # setup unittest message mechanism
        self.test_mode = False
        self.test_message = None

    @staticmethod
    def quit():
        QCoreApplication.instance().quit()

    def add_matplotlib_canvas(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ui.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.addToolBar(NavigationToolbar(self.canvas, self, coordinates=True))

    def store_initial_widget_values(self, args):
        self.ui.edit_XMin.setText(str(self.x_range[0]))
        self.ui.edit_XMax.setText(str(self.x_range[1]))
        self.ui.edit_YMin.setText(str(self.y_range[0]))
        self.ui.edit_YMax.setText(str(self.y_range[1]))
        self.ui.edit_XBins.setText(str(args.xbins))
        self.ui.edit_YBins.setText(str(args.ybins or ""))
        self.ui.radioButton_linear.setChecked(True)
        if args.power is not None:
            self.ui.radioButton_power.setChecked(True)
            self.ui.edit_Exp.setText(args.power)
        self.ui.radioButton_log.setChecked(args.log)
        self.ui.radioButton_loglog.setChecked(args.loglog)
        self.ui.edit_VMax.setText(args.vmax)
        self.ui.edit_colormap.setText(args.colormap)

    def connect_signals(self):
        partial = functools.partial

        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.buttonReplot.clicked.connect(self.replot)
        self.ui.buttonUndo.clicked.connect(self.undo)

        self.ui.slider_XMin.valueChanged.connect(self.slidervaluechangeXmin)
        self.ui.slider_XMax.valueChanged.connect(self.slidervaluechangeXMax)
        self.ui.slider_YMin.valueChanged.connect(self.slidervaluechangeYmin)
        self.ui.slider_YMax.valueChanged.connect(self.slidervaluechangeYMax)
        self.ui.edit_XMin.editingFinished.connect(self.labelfinishedXmin)
        self.ui.edit_XMax.editingFinished.connect(self.labelfinishedXMax)
        self.ui.edit_YMin.editingFinished.connect(self.labelfinishedYmin)
        self.ui.edit_YMax.editingFinished.connect(self.labelfinishedYMax)

        self.ui.actionMeasure.triggered.connect(partial(self.activate_or_deactivate, self.measure_distance_handler))
        self.ui.actionRange.triggered.connect(partial(self.activate_or_deactivate, self.rectangle_zoom_handler))
        self.ui.actionCount.triggered.connect(partial(self.activate_or_deactivate, self.count_pairs_handler))
        self.ui.checkBox_query_phtree.clicked.connect(partial(self.activate_or_deactivate, self.phtrees_handler))
        self.ui.checkBox_show_ancestors.clicked.connect(self.draw_canvas)
        self.ui.checkBox_show_descendants.clicked.connect(self.draw_canvas)
        self.ui.button_show_descendants.clicked.connect(self.phtrees_handler.show_descendants_volumes)
        self.ui.checkBox_query_volumes_in_rectangle.clicked.connect(
            partial(self.activate_or_deactivate, self.phtrees_range_query_handler)
        )
        self.ui.checkBox_optimal_volume_on.clicked.connect(
            partial(self.activate_or_deactivate, self.optimal_volume_handler)
        )
        self.ui.checkBox_optimal_volume_show_children.clicked.connect(self.draw_canvas)

        self.canvas.mpl_connect("button_press_event", self.on_mouse_button_press)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_button_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.canvas.mpl_connect("axes_leave_event", self.on_mouse_leave)
        self.canvas.mpl_connect("draw_event", self.on_draw)
        self.canvas.mpl_connect("figure_enter_event", self.figure_enter)
        self.canvas.mpl_connect("figure_leave_event", self.figure_leave)

    def invalidate_phtrees_widgets(self):
        self.ui.checkBox_query_phtree.setEnabled(False)
        self.ui.button_show_descendants.setEnabled(False)
        self.ui.checkBox_show_ancestors.setEnabled(False)
        self.ui.checkBox_show_descendants.setEnabled(False)
        self.ui.checkBox_query_volumes_in_rectangle.setEnabled(False)
        self.ui.frame_phtree.setHidden(True)

    def invalidate_optimal_volume_widgets(self):
        self.ui.frame_optimal_volume.setHidden(True)

    def draw_canvas(self):
        try:
            inputbox_state = InputBoxState(self.ui)
        except ValueError as err:
            self.error_dialog("parameter convert error: {}".format(str(err)))
            return None

        histogram = PDHistogram(self.pd, *inputbox_state.xy_rulers(self.pd))
        histogram.multiply_histogram(1.0 / self.normalize_constant)

        if inputbox_state.apply_diffusion:
            histogram.apply_gaussian_filter(inputbox_state.diffusion_sigma)

        self.figure.clf()
        self.ax = self.figure.add_subplot(111)

        inputbox_state.plotter_class()(histogram, inputbox_state.zspec(), self.aux_plot_info).plot(
            self.figure, self.ax
        )

        self.phtrees_handler.draw_ancestors(self.ax)
        self.phtrees_handler.draw_descendants(self.ax)
        self.optimal_volume_handler.draw_children(self.ax)

        self.canvas.draw()
        self.save_backgroud()
        self.current_canvas_ev_handler.reset()
        return inputbox_state

    def save_backgroud(self):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def restore_background(self):
        self.canvas.restore_region(self.background)

    def blit_canvas(self):
        self.canvas.blit(self.ax.bbox)

    def replot(self):
        inputbox_state = self.draw_canvas()
        if not inputbox_state:
            return
        self.replot_history.append(inputbox_state)
        self.set_buttonUndo()

    def set_buttonUndo(self):
        self.ui.buttonUndo.setEnabled(len(self.replot_history) >= 2)

    def xmin(self):
        return float(self.ui.edit_XMin.text())

    def xmax(self):
        return float(self.ui.edit_XMax.text())

    def ymin(self):
        return float(self.ui.edit_YMin.text())

    def ymax(self):
        return float(self.ui.edit_YMax.text())

    def undo(self):
        def adjust_sliders():
            self.labelfinishedXmin()
            self.labelfinishedXMax()
            self.labelfinishedYmin()
            self.labelfinishedYMax()

        self.replot_history.pop()
        self.replot_history[-1].restore(self.ui)
        adjust_sliders()
        self.draw_canvas()
        self.set_buttonUndo()

    def error_dialog(self, msg):
        if self.test_mode:
            self.test_message = msg
            return

        dialog = QMessageBox(self)
        dialog.setText(msg)
        dialog.exec_()

    def slidervaluechangeXmin(self):
        self.adjust_editline_by_slider(self.ui.slider_XMin, self.ui.edit_XMin, self.x_range)

    def slidervaluechangeXMax(self):
        self.adjust_editline_by_slider(self.ui.slider_XMax, self.ui.edit_XMax, self.x_range)

    def slidervaluechangeYmin(self):
        self.adjust_editline_by_slider(self.ui.slider_YMin, self.ui.edit_YMin, self.y_range)

    def slidervaluechangeYMax(self):
        self.adjust_editline_by_slider(self.ui.slider_YMax, self.ui.edit_YMax, self.y_range)

    @staticmethod
    def slider_to_value(val, range_):
        left, right = range_
        return left + val / 100.0 * (right - left)

    def adjust_editline_by_slider(self, slider, editline, range_):
        editline.setText(str(self.slider_to_value(slider.value(), range_)))

    def labelfinishedXmin(self):
        self.adjust_slider_by_edit(self.ui.slider_XMin, self.ui.edit_XMin, self.x_range)

    def labelfinishedXMax(self):
        self.adjust_slider_by_edit(self.ui.slider_XMax, self.ui.edit_XMax, self.x_range)

    def labelfinishedYmin(self):
        self.adjust_slider_by_edit(self.ui.slider_YMin, self.ui.edit_YMin, self.y_range)

    def labelfinishedYMax(self):
        self.adjust_slider_by_edit(self.ui.slider_YMax, self.ui.edit_YMax, self.y_range)

    def adjust_slider_by_edit(self, slider, editline, range_):
        try:
            value = float(editline.text())
        except ValueError:
            self.adjust_editline_by_slider(slider, editline, range_)
            self.error_dialog("Input data error")
            return
        slider.setSliderPosition(self.value_to_slider(value, range_))

    def set_slider_and_edit_by_range(self, slider, editline, value, range_):
        slider.setSliderPosition(self.value_to_slider(value, range_))
        editline.setText(str(value))

    @staticmethod
    def value_to_slider(val, range_):
        left, right = range_
        return int(100 * (val - left) / (right - left))

    def canvas_event_handlers(self):
        return [
            self.measure_distance_handler,
            self.rectangle_zoom_handler,
            self.count_pairs_handler,
            self.phtrees_handler,
            self.phtrees_range_query_handler,
            self.optimal_volume_handler,
        ]

    def activate_or_deactivate(self, handler, checked):
        if checked:
            handler.activate()
            for h in self.canvas_event_handlers():
                if h != handler:
                    h.activator_widget().setChecked(False)
        else:
            self.deactivate_mouse_handler()

    def on_mouse_button_press(self, event):
        self.current_canvas_ev_handler.on_button_press(event)

    def on_mouse_button_release(self, event):
        self.current_canvas_ev_handler.on_button_release(event)

    def on_mouse_move(self, event):
        self.current_canvas_ev_handler.on_mouse_move(event)

    def on_mouse_leave(self, event):
        self.current_canvas_ev_handler.on_mouse_leave(event)

    def deactivate_mouse_handler(self):
        self.current_canvas_ev_handler = NoOpMouseHandler()

    def on_draw(self, event):
        self.save_backgroud()

    def set_ui_ranges(self, x_range, y_range):
        self.set_slider_and_edit_by_range(self.ui.slider_XMin, self.ui.edit_XMin, x_range[0], self.x_range)
        self.set_slider_and_edit_by_range(self.ui.slider_XMax, self.ui.edit_XMax, x_range[1], self.x_range)
        self.set_slider_and_edit_by_range(self.ui.slider_YMin, self.ui.edit_YMin, y_range[0], self.y_range)
        self.set_slider_and_edit_by_range(self.ui.slider_YMax, self.ui.edit_YMax, y_range[1], self.y_range)

    def figure_enter(self, event):
        del event
        if self.ui.actionRange.isChecked():
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        elif self.ui.actionMeasure.isChecked():
            open_hand_px = QPixmap(":ui/cursor_measure.png")
            open_hand_px.setMask(open_hand_px.mask())
            QApplication.setOverrideCursor(QCursor(open_hand_px))

    def figure_leave(self, event):
        del event
        if self.ui.actionRange.isChecked() or self.ui.actionMeasure.isChecked():
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

    def get_test_message_and_clear(self):
        msg = self.test_message
        self.test_message = None
        return msg


class BaseMouseHandler(object):
    def is_valid_click_event(self, event):
        return (
            self.window.ax is not None
            and event.inaxes == self.window.ax
            and event.button == 1
            and event.xdata is not None
            and event.ydata is not None
        )

    def on_button_press(self, event):
        pass

    def on_mouse_move(self, event):
        pass

    def on_button_release(self, event):
        pass

    def on_mouse_leave(self, event):
        pass

    def reset(self):
        pass


class NullWidget(object):
    @staticmethod
    def setChecked(_):
        pass


class MouseDragHandler(BaseMouseHandler):
    def __init__(self, window):
        self.window = window
        self.start_xy = None

    def on_button_press(self, event):
        if not self.is_valid_click_event(event):
            return

        self.start_xy = (event.xdata, event.ydata)
        self.press()

    @staticmethod
    def press():
        pass

    def on_mouse_move(self, event):
        if not self.is_dragging(event):
            return

        mouse_xy = (event.xdata, event.ydata)
        self.draw(self.start_xy, mouse_xy)
        self.move(mouse_xy)

    @staticmethod
    def move(mouse_xy):
        pass

    def is_dragging(self, event):
        return event.inaxes == self.window.ax and self.start_xy

    def on_button_release(self, event):
        if not self.is_dragging(event):
            return

        start_xy = self.start_xy
        self.clear()
        self.release(start_xy, (event.xdata, event.ydata))

    @staticmethod
    def release(start_xy, end_xy):
        pass

    def on_mouse_leave(self, event):
        self.clear()

    def clear(self):
        self.start_xy = None
        self.window.restore_background()
        self.window.blit_canvas()

    def draw(self, start, end):
        self.window.restore_background()
        self.drawer.draw(start, end)
        self.window.blit_canvas()

    def reset(self):
        self.start_xy = None
        self.drawer.reset()

    class LineDrawer(object):
        def __init__(self, window):
            self.window = window
            self.line = None

        def reset(self):
            self.line = Line2D((0, 0), (0, 0), linewidth=1, color="black", linestyle="dotted")
            self.window.ax.add_line(self.line)

        def draw(self, start, end):
            self.line.set_xdata([start[0], end[0]])
            self.line.set_ydata([start[1], end[1]])
            self.window.ax.draw_artist(self.line)

    class RectangleDrawer(object):
        def __init__(self, window):
            self.window = window
            self.rect = None

        def reset(self):
            self.rect = Rectangle((0, 0), 0, 0, fill=False, linewidth="1.0", edgecolor="blue", linestyle="dotted")
            self.window.ax.add_patch(self.rect)

        def draw(self, start, end):
            xmin, xmax = minmax(start[0], end[0])
            ymin, ymax = minmax(start[1], end[1])
            self.rect.set_bounds(xmin, ymin, xmax - xmin, ymax - ymin)
            self.window.ax.draw_artist(self.rect)


class NoOpMouseHandler(BaseMouseHandler):
    pass


class MouseClickHandler(BaseMouseHandler):
    def __init__(self, window):
        self.window = window

    def on_button_press(self, event):
        if not self.is_valid_click_event(event):
            return
        self.click((event.xdata, event.ydata))

    def click(self, mouse_xy):
        pass


class MeasureDistanceHandler(object):
    def __init__(self, window):
        self.window = window

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self.window)
        self.window.current_canvas_ev_handler.reset()

    def activator_widget(self):
        return self.window.ui.actionMeasure

    class MouseHandler(MouseDragHandler):
        def __init__(self, window):
            super().__init__(window)
            self.drawer = MouseDragHandler.LineDrawer(window)
            self.statusbar = window.ui.statusbar

        def show_distance(self, begin, end):
            def distance(u, v):
                return np.linalg.norm(np.array(u) - np.array(v))

            self.statusbar.showMessage("coord: {} - {},  distance: {}".format(begin, end, distance(begin, end)))

        def move(self, mouse_xy):
            self.show_distance(self.start_xy, mouse_xy)

        def press(self):
            self.show_distance(self.start_xy, self.start_xy)


class CountPairsHandler(object):
    def __init__(self, window):
        self.window = window

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self.window)
        self.window.current_canvas_ev_handler.reset()

    def activator_widget(self):
        return self.window.ui.actionCount

    class MouseHandler(MouseDragHandler):
        def __init__(self, window):
            super().__init__(window)
            self.drawer = MouseDragHandler.RectangleDrawer(window)
            self.pd = window.pd
            self.statusbar = window.ui.statusbar
            self.timer = None

        def move(self, mouse_xy):
            self.stop_timer()
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.setInterval(100)
            self.timer.timeout.connect(functools.partial(self.show_pairs_in_rectangle, mouse_xy))
            self.timer.start()

        def show_pairs_in_rectangle(self, mouse_xy):
            if not self.start_xy:
                return

            num_pairs = self.pd.count_pairs_in_rectangle(self.start_xy[0], mouse_xy[0], self.start_xy[1], mouse_xy[1])
            self.statusbar.showMessage("coord: {} - {},  count: {}".format(self.start_xy, mouse_xy, num_pairs))

        def stop_timer(self):
            if self.timer:
                self.timer.stop()


class PHTreesHandler(object):
    def __init__(self, resolver, tmpdir, window):
        self.resolver = resolver
        self.leaf_for_query_ancestors = None
        self.root_for_query_descendants = None
        self.tmpdir = tmpdir
        self.window = window

    @staticmethod
    def is_available():
        return True

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self)

    def activator_widget(self):
        return self.window.ui.checkBox_query_phtree

    def query(self, birth, death):
        self.leaf_for_query_ancestors = self.resolver.query_node(birth, death)
        self.root_for_query_descendants = self.resolver.query_node(birth, death)

    def show_descendants_volumes(self):
        if not self.root_for_query_descendants:
            return
        tmpfile = tmppath(self.tmpdir, ".vtk")
        self.root_for_query_descendants.draw_descendants_volumes(self.resolver.index_map.points, tmpfile, False, False)
        utils.invoke_paraview(tmpfile)

    def draw_ancestors(self, ax):
        if not self.window.ui.checkBox_show_ancestors.isChecked():
            return

        if not self.leaf_for_query_ancestors:
            return

        def visit_node(node):
            ax.scatter([node.birth_time()], [node.death_time()], c="blue", edgecolors="black")
            if node.parent:
                ax.plot(
                    [node.birth_time(), node.parent.birth_time()],
                    [node.death_time(), node.parent.death_time()],
                    c="black",
                )
                visit_node(node.parent)

        visit_node(self.leaf_for_query_ancestors)

    def draw_descendants(self, ax):
        if not self.window.ui.checkBox_show_descendants.isChecked():
            return

        if not self.root_for_query_descendants:
            return

        def visit_node(node):
            ax.scatter([node.birth_time()], [node.death_time()], c="red", edgecolors="black")

            for child in node.children:
                if not child.living():
                    continue
                ax.plot([node.birth_time(), child.birth_time()], [node.death_time(), child.death_time()], c="black")
                visit_node(child)

        visit_node(self.root_for_query_descendants)

    class MouseHandler(MouseClickHandler):
        def __init__(self, phtrees_handler):
            super().__init__(phtrees_handler.window)
            self.phtrees_handler = phtrees_handler

        def click(self, mouse_xy):
            self.phtrees_handler.query(*mouse_xy)
            self.window.draw_canvas()

    @staticmethod
    def create(resolver, tmpdir, window):
        if resolver is None:
            return PHTreesHandler.NoOp()
        else:
            return PHTreesHandler(resolver, tmpdir, window)

    class NoOp(object):
        @staticmethod
        def is_available():
            return False

        @staticmethod
        def activate():
            pass

        @staticmethod
        def activator_widget():
            return NullWidget()

        @staticmethod
        def show_descendants_volumes():
            pass

        @staticmethod
        def draw_ancestors(ax):
            del ax

        @staticmethod
        def draw_descendants(ax):
            del ax


class PHTreesRangeQueryHandler(object):
    def __init__(self, resolver, tmpdir, window):
        self.resolver = resolver
        self.tmpdir = tmpdir
        self.window = window

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self)
        self.window.current_canvas_ev_handler.reset()

    def activator_widget(self):
        return self.window.ui.checkBox_query_volumes_in_rectangle

    def show_volumes_in_rectangle(self, v1, v2):
        xmin, xmax = minmax(v1[0], v2[0])
        ymin, ymax = minmax(v1[1], v2[1])
        nodes = self.resolver.query_nodes_in_rectangle(xmin, xmax, ymin, ymax)
        tmpfile = tmppath(self.tmpdir, ".vtk")
        self.resolver.draw_volumes_of_nodes(nodes, tmpfile, True, True)
        utils.invoke_paraview(tmpfile)

    class MouseHandler(MouseDragHandler):
        def __init__(self, phtrees_range_handler):
            super().__init__(phtrees_range_handler.window)
            self.drawer = MouseDragHandler.RectangleDrawer(phtrees_range_handler.window)
            self.phtrees_range_handler = phtrees_range_handler

        def release(self, start_xy, end_xy):
            self.phtrees_range_handler.show_volumes_in_rectangle(start_xy, end_xy)

    @staticmethod
    def create(resolver, tmpdir, ui):
        if resolver is None:
            return PHTreesRangeQueryHandler.NoOp()
        else:
            return PHTreesRangeQueryHandler(resolver, tmpdir, ui)

    class NoOp(object):
        @staticmethod
        def activate():
            pass

        @staticmethod
        def activator_widget():
            return NullWidget()


class RectangleZoomHandler(object):
    def __init__(self, window):
        self.window = window

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self.window)
        self.window.current_canvas_ev_handler.reset()

    def activator_widget(self):
        return self.window.ui.actionRange

    class MouseHandler(MouseDragHandler):
        def __init__(self, window):
            super().__init__(window)
            self.drawer = MouseDragHandler.RectangleDrawer(window)

        def release(self, start_xy, end_xy):
            self.window.set_ui_ranges(minmax(start_xy[0], end_xy[0]), minmax(start_xy[1], end_xy[1]))
            self.window.replot()


class OptimalCycleHandler(object):
    def __init__(self, diagram_path, degree, window, tmpdir, options):
        self.diagram_path = diagram_path
        self.window = window
        self.degree = degree
        self.tmpdir = tmpdir
        self.options = options
        self.voc_info = None

    def activate(self):
        self.window.current_canvas_ev_handler = self.MouseHandler(self)

    def activator_widget(self):
        return self.window.ui.checkBox_optimal_volume_on

    def query(self, pos):
        vtkpath = tmppath(self.tmpdir, ".vtk")
        jsonpath = tmppath(self.tmpdir, ".json")
        options = self.options.copy()

        if self.window.ui.checkBox_optimal_volume_query_children.isChecked():
            options.extend(["-C", "on"])

        eigenvolume_th = self.window.ui.lineEdit_optimal_volume_stable_volume.text()
        if self.is_eigenvolume_none():
            pass
        elif self.window.ui.radioButton_eigenvolume_tightened.isChecked():
            options.extend(
                [
                    "--tightened-volume",
                    eigenvolume_th,
                    "--no-optimal-volume",
                    "yes",
                    "--show-optimal-volume",
                    "no",
                ]
            )
        elif self.window.ui.radioButton_eigenvolume_owned.isChecked():
            options.extend(
                [
                    "--owned-volume",
                    eigenvolume_th,
                    "--show-optimal-volume",
                    "no",
                ]
            )
        elif self.window.ui.radioButton_eigenvolume_tightened_sub.isChecked():
            options.extend(
                [
                    "--tightened-subvolume",
                    eigenvolume_th,
                    "--show-optimal-volume",
                    "no",
                ]
            )

        process = QProcess()
        process.setProcessChannelMode(QProcess.ForwardedChannels)
        dialog = QProgressDialog("Computing volume optimal cycle...", "Cancal", 0, 0)
        process.finished.connect(dialog.reset)
        dialog.canceled.connect(process.kill)

        process.start(
            sys.executable,
            [
                "-m",
                "homcloud.optimal_volume",
                "-d",
                str(self.degree),
                "-x",
                str(pos[0]),
                "-y",
                str(pos[1]),
                "-v",
                vtkpath,
                "-n",
                self.window.ui.lineEdit_optimal_volume_retry.text(),
                "--cutoff-radius",
                self.window.ui.lineEdit_optimal_volume_cutoff_radius.text(),
                "-j",
                jsonpath,
                self.diagram_path,
            ]
            + options,
        )
        if not process.waitForStarted():
            self.show_optimal_volume_error(-1)
            return
        dialog.exec()
        if process.waitForFinished():
            return
        elif process.exitCode() == 0:
            if self.is_eigenvolume_none():
                self.load_info_from_jsonfile(jsonpath)
            self.window.draw_canvas()
            if self.window.ui.checkBox_optimal_volume_show_volume.isChecked():
                utils.invoke_paraview(vtkpath)
        else:
            self.show_optimal_volume_error(process.exitCode())
        # Here, the above code is difficult to understand, hence we explain as follow:
        #
        # First, by `procees.start`, the optimal cycle program starts in prallel with
        # the GUI process.
        # Next, call QProcess.waitForStarted to check the program is successfully started
        # Next, by `dialog.exec`, the dialog is invoked.
        # This dialog is modal, we will wait for finishing the process or
        # we click cancel button.
        #   * Then, if the program finishes, then dialog is closed from
        #     the QProcess#finished signal
        #     * In this case, process.waitForFinished returns false since the process is
        #       already stopped
        #
        #   * If the cancel button is clicked, the process is killed from
        #     QProgressDialog#canceled signal
        #     * In this case, process.waitForFinished returns true or false
        #       * It return true when kill signal is sent but the process is not yet killed
        #         because of the timing problem
        #       * Otherwise, it returns false
        # In both case, after `dialog.exec()`, the process is "almost" stopped.

    def show_optimal_volume_error(self, exitcode):
        if exitcode == 10:
            msg = "Death simplex out of cutoff ball"
        elif exitcode == 2:
            msg = "Infeasible (probably cutoff radius is too small)"
        elif exitcode == -1:
            msg = "Process invoke error"
        else:
            msg = "Unknown code: {}".format(exitcode)

        self.window.error_dialog(msg)

    def load_info_from_jsonfile(self, path):
        with open(path) as f:
            self.voc_info = json.load(f)["result"]

    def is_eigenvolume_none(self):
        return self.window.ui.radioButton_eigenvolume_none.isChecked()

    def draw_children(self, ax):
        if not self.voc_info:
            return
        if not self.window.ui.checkBox_optimal_volume_show_children.isChecked():
            return

        ax.scatter([self.voc_info[0]["birth-time"]], [self.voc_info[0]["death-time"]], c="green", edgecolor="black")
        for child in self.voc_info[0]["children"]:
            ax.scatter([child["birth-time"]], [child["death-time"]], c="red", edgecolor="black")

    @staticmethod
    def is_available():
        return True

    class MouseHandler(MouseClickHandler):
        def __init__(self, optimal_volume_handler):
            super().__init__(optimal_volume_handler.window)
            self.optimal_volume_handler = optimal_volume_handler

        def click(self, mouse_xy):
            self.optimal_volume_handler.query(mouse_xy)

    @staticmethod
    def create(pd, window, tmpdir, activate, options):
        def optimal_volume_available():
            return pd.filtration_type == "alpha" and pd.path

        if optimal_volume_available() and activate:
            return OptimalCycleHandler(pd.path, pd.degree, window, tmpdir, options)
        else:
            return OptimalCycleHandler.NoOp()

    class NoOp(object):
        @staticmethod
        def clicked(pos):
            del pos

        @staticmethod
        def is_available():
            return False

        @staticmethod
        def activator_widget():
            return NullWidget()

        @staticmethod
        def draw_children(ax):
            return

    class Dialog(QDialog):
        pass


class InputBoxState(object):
    def __init__(self, ui):
        self.normalplot = ui.radioButton_normalplot.isChecked()
        self.contourplot = ui.radioButton_contourplot.isChecked()
        self.linear_z = ui.radioButton_linear.isChecked()
        self.log_z = ui.radioButton_log.isChecked()
        self.loglog_z = ui.radioButton_loglog.isChecked()
        self.power_z = ui.radioButton_power.isChecked()
        self.power_z_exp_text = ui.edit_Exp.text()
        self.z_max_text = ui.edit_VMax.text()
        self.apply_diffusion = ui.checkBox_Diffusing.isChecked()
        self.diffusing_sigma_text = ui.edit_DiffusingSize.text()
        self.xmin_text = ui.edit_XMin.text()
        self.xmax_text = ui.edit_XMax.text()
        self.xrange_eq_yrange = ui.checkBox_yrange.isChecked()
        self.ymin_text = ui.edit_YMin.text()
        self.ymax_text = ui.edit_YMax.text()
        self.xbins_text = ui.edit_XBins.text()
        self.ybins_text = ui.edit_YBins.text()
        self.colormap = ui.edit_colormap.text()
        self.validate_colormap()

        if self.power_z:
            self.power_z_exp = float(self.power_z_exp_text)

        self.z_max = float(self.z_max_text) if self.z_max_text else None

        if self.apply_diffusion:
            self.diffusion_sigma = float(self.diffusing_sigma_text)
        else:
            self.diffusion_sigma = None

        self.xmin = float(self.xmin_text)
        self.xmax = float(self.xmax_text)
        self.ymin = self.xmin if self.xrange_eq_yrange else float(self.ymin_text)
        self.ymax = self.xmax if self.xrange_eq_yrange else float(self.ymax_text)
        self.xbins = int(self.xbins_text)
        self.ybins = int(self.ybins_text) if self.ybins_text else None

    def validate_colormap(self):
        if self.colormap:
            plt.get_cmap(self.colormap)

    def xy_rulers(self, diagram):
        return Ruler.create_xy_rulers((self.xmin, self.xmax), self.xbins, (self.ymin, self.ymax), self.ybins, diagram)

    def zspec(self):
        colormap = plt.get_cmap(self.colormap) if self.colormap else None

        if self.linear_z:
            return ZSpec.Linear(self.z_max, None, colormap)
        if self.log_z and self.apply_diffusion:
            return ZSpec.LogWithDiffusion(self.z_max, None, colormap)
        if self.log_z:
            return ZSpec.Log(self.z_max, None, colormap)
        if self.loglog_z:
            return ZSpec.LogLog(self.z_max, None, colormap)
        if self.power_z:
            return ZSpec.Power(self.power_z_exp, self.z_max, None, colormap)
        raise ValueError("zspec radiobutton error")

    def plotter_class(self):
        if self.normalplot:
            return PDColorHistogramPlotter
        if self.contourplot:
            return PDContourPlotter
        raise ValueError("plot style radiobutton error")

    def restore(self, ui):
        ui.radioButton_normalplot.setChecked(self.normalplot)
        ui.radioButton_contourplot.setChecked(self.contourplot)
        ui.radioButton_linear.setChecked(self.linear_z)
        ui.radioButton_log.setChecked(self.log_z)
        ui.radioButton_loglog.setChecked(self.loglog_z)
        ui.radioButton_power.setChecked(self.power_z)
        ui.edit_Exp.setText(self.power_z_exp_text)
        ui.edit_VMax.setText(self.z_max_text)
        ui.edit_colormap.setText(self.colormap)
        ui.checkBox_Diffusing.setChecked(self.apply_diffusion)
        ui.edit_DiffusingSize.setText(self.diffusing_sigma_text)
        ui.edit_XMin.setText(self.xmin_text)
        ui.edit_XMax.setText(self.xmax_text)
        ui.checkBox_yrange.setChecked(self.xrange_eq_yrange)
        ui.edit_YMin.setText(self.ymin_text)
        ui.edit_YMax.setText(self.ymax_text)
        ui.edit_XBins.setText(self.xbins_text)


def minmax(x, y):
    return min(x, y), max(x, y)


def tmppath(tmpdir, suffix):
    return os.path.join(tmpdir, str(uuid.uuid4()) + suffix)


def argument_parser():
    p = argparse.ArgumentParser(description="View PD interactively", conflict_handler="resolve")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    p.add_argument("--power", default=None, help="colorbar scale: x^POWER for each value x")
    p.add_argument("-l", "--log", action="store_true", default=False, help="colorbar scale: log(x+1) for each value x")
    p.add_argument("--loglog", action="store_true", default=False, help="colorbar scale: log(log(x+1)+1)")
    p.add_argument("-m", "--vmax", metavar="MAX", default="", help="Maximum of colorbar (default: autoscale)")
    p.add_argument("-c", "--colormap", default="", help="matplotlib colormap name")
    add_arguments_for_histogram_rulers(p)
    add_arguments_for_auxinfo(p)
    p.add_argument(
        "-n", "--normalize-constant", type=float, default=1.0, help="normalize constant to histogram height"
    )
    p.add_argument("-p", "--ph-trees", help="ph trees file (.pht)")
    p.add_argument(
        "--optimal-volume", "--optimal-cycle", default=False, type=parse_bool, help="activate optimal volume (on/off)"
    )
    p.add_argument("--optimal-volume-options", default="", help="options for optimal_volume module")
    p.add_argument("input", nargs="+", help="input file")
    return p


def main():
    app = QApplication(sys.argv)
    args = argument_parser().parse_args(app.arguments()[1:])
    if args.title is None:
        args.title = args.input[0]

    pd = pdgm.load_merged_diagrams(args.input, args.type, args.degree)

    # if args.ph_trees:
    #     with open(args.ph_trees, "rb") as f:
    #         phtrees_resolver = full_ph_tree.TreeResolver.load(f)
    # else:
    #     phtrees_resolver = None
    phtrees_resolver = None

    with tempfile.TemporaryDirectory() as tmpdir:
        main_window = MainWindow(pd, phtrees_resolver, tmpdir, args)
        app.lastWindowClosed.connect(MainWindow.quit)

        main_window.replot()
        main_window.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
