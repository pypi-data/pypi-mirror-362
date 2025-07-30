# pylint: disable=C0103,C0111,C0411,W0201,R0201,R0903,C0412
import re

import pytest

from homcloud.pdgm import PDGM

from .conftest import picture_dir

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QAction
    from homcloud.plot_PD_gui import MainWindow, argument_parser
except ImportError:
    pass


@pytest.mark.gui
class TestPlotPDGUI:
    @staticmethod
    def args(args):
        return argument_parser().parse_args(args + ["-d", "0", "dummy"])

    def window(self, qtbot, path_bin_pdgm, tmpdir):
        diagram = PDGM.open(path_bin_pdgm, 0)
        main_window = MainWindow(diagram, None, str(tmpdir), self.args([]))
        qtbot.addWidget(main_window)

        main_window.test_mode = True
        main_window.replot()
        return main_window

    @staticmethod
    def save_screenshot(window, path):
        window.grab().save(str(picture_dir().joinpath(path)))

    def test_initial_state(self, qtbot, path_bin_pdgm, tmpdir):
        window = self.window(qtbot, path_bin_pdgm, tmpdir)
        assert window.ui.radioButton_normalplot.isChecked()
        assert not window.ui.radioButton_contourplot.isChecked()
        assert window.ui.radioButton_linear.isChecked()
        assert not window.ui.checkBox_yrange.isChecked()
        assert window.ui.edit_VMax.text() == ""
        assert window.ui.edit_XBins.text() == "128"
        assert not window.ui.buttonUndo.isEnabled()

    @staticmethod
    def keyclicks_clear_and_input_in_editline(qtbot, editline, string):
        qtbot.keyClick(editline, "a", Qt.ControlModifier)
        qtbot.keyClicks(editline, string)
        qtbot.keyClick(editline, Qt.Key_Enter)

    def test_senario1(self, qtbot, path_bin_pdgm, tmpdir):
        window = self.window(qtbot, path_bin_pdgm, tmpdir)

        # Use log plot, xmin and xmax are changed
        window.ui.radioButton_log.click()
        self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XBins, "32")
        self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XMin, "-12")
        self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XMax, "6")
        qtbot.mouseClick(window.ui.buttonReplot, Qt.LeftButton)
        assert window.ui.edit_XMin.text() == "-12.0"
        assert window.ui.edit_XMax.text() == "6"
        assert window.ui.buttonUndo.isEnabled()
        self.save_screenshot(window, "plot_PD_gui-screen-01-01.png")

        # Undo
        qtbot.mouseClick(window.ui.buttonUndo, Qt.LeftButton)
        assert window.ui.edit_XBins.text() == "128"
        assert not window.ui.buttonUndo.isEnabled()
        assert window.ui.edit_XMin.text() == "-19.0"
        assert window.ui.edit_XMax.text() == "6.0"
        self.save_screenshot(window, "plot_PD_gui-screen-01-02.png")

        # Use Measure
        window.ui.actionMeasure.activate(QAction.Trigger)
        window.canvas.button_press_event(100, 500, 1)
        window.canvas.motion_notify_event(200, 200)
        self.save_screenshot(window, "plot_PD_gui-screen-01-03.png")
        window.canvas.button_release_event(200, 200, 1)
        self.save_screenshot(window, "plot_PD_gui-screen-01-04.png")

        # Use Range
        window.ui.checkBox_yrange.setChecked(False)
        window.ui.actionRange.activate(QAction.Trigger)
        window.canvas.button_press_event(100, 500, 1)
        window.canvas.motion_notify_event(400, 200)
        qtbot.wait(600)
        self.save_screenshot(window, "plot_PD_gui-screen-01-05.png")
        window.canvas.button_release_event(400, 200, 1)
        xmin = float(window.ui.edit_XMin.text())
        xmax = float(window.ui.edit_XMax.text())
        ymin = float(window.ui.edit_YMin.text())
        ymax = float(window.ui.edit_YMax.text())
        assert -19.0 < xmin < xmax < 6.0
        assert -19.0 < ymin < ymax < 6.0
        assert xmin != ymin
        assert xmax != ymax
        self.save_screenshot(window, "plot_PD_gui-screen-01-06.png")

        # Show Error in edit_XMin
        self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XMin, "foobar")
        assert window.get_test_message_and_clear() == "Input data error"

        self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XBins, "foobar")
        assert window.get_test_message_and_clear() is None
        qtbot.mouseClick(window.ui.buttonReplot, Qt.LeftButton)
        assert re.match("parameter convert error: ", window.get_test_message_and_clear())

    # @unittest.mock.patch("homcloud.utils.invoke_paraview")
    # def test_senario2(self, mock_invoke, qtbot, datadir, tmpdir):
    #     window = self.window_with_phtree(qtbot, datadir, tmpdir)
    #     assert not window.ui.checkBox_query_phtree.isChecked()
    #     assert window.ui.checkBox_show_ancestors.isChecked()

    #     self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XBins, "64")
    #     self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XMin, "18")
    #     self.keyclicks_clear_and_input_in_editline(qtbot, window.ui.edit_XMax, "23")
    #     window.ui.checkBox_yrange.setChecked(True)
    #     qtbot.mouseClick(window.ui.buttonReplot, Qt.LeftButton)

    #     qtbot.mouseClick(window.ui.checkBox_query_phtree, Qt.LeftButton)
    #     window.canvas.button_press_event(100, 100, 1)
    #     qtbot.wait(100)
    #     self.save_screenshot(window, "plot_PD_gui-screen-02-01.png")

    #     assert not mock_invoke.called
    #     qtbot.mouseClick(window.ui.button_show_descendants, Qt.LeftButton)
    #     assert mock_invoke.called
