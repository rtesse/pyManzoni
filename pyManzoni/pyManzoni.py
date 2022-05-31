import sys
from PySide2 import QtWidgets
from ui.pyManzoni_MainUi import MainWindow
from tracker import Tracker


class PyManzoni(MainWindow):

    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        # # Define the kinematics
        # self.called = False
        #
        # # Define the class for the sequence
        self.tracker = Tracker(layout_results=self.layout_widget, layout_sequence=self.s_ui)
        #
        # # Connect buttons and actions
        # # self.connect_shortcut()
        self.connect_button()

    def connect_button(self):
        # self.ui.element_list.activated.connect(self.tracker.set_plotting_element)
        self.tracking_button.setCheckable(True)
        self.tracking_button.toggle()
        self.tracking_button.clicked.connect(self.track)

    def track(self):
        self.tracker(sequence=self.s_ui.sequence,
                     beam=self.b_ui.beam,
                     kinematics=self.k_ui.kinematics)

    # def vtk_button(self):
    #     if not self.tracker.vtk_viewer.init_vtk:
    #         self.tracker.vtk_viewer.setupUi()
    #         self.tracker.vtk_viewer.show()
    #     else:
    #         self.tracker.vtk_viewer.showMaximized()
    #
    # def view_all(self):
    #     self.ui.dockWidget_line.setVisible(True)
    #     self.ui.dockWidget_sequence.setVisible(True)
    #
    # def close_app(self):
    #     msgbox = QMessageBox(QMessageBox.Warning, "", "Are you sure you want to quit ? ",
    #                          buttons=QMessageBox.No | QMessageBox.Yes,
    #                          parent=self)
    #     msgbox.setDefaultButton(QMessageBox.No)
    #     if msgbox.exec_() == QMessageBox.Yes:
    #         app.quit()
    #
    # def clean_tmp_files(self):
    #     self.ui.clean_tmp_files()
    #
    # def closeEvent(self, event):
    #     # do stuff
    #     self.ui.clean_tmp_files()
    #     if self.ui.plotwindows is not None and self.ui.plotwindows.isVisible:
    #         self.ui.plotwindows.close()
    #     event.accept()  # let the window close


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = PyManzoni()
    myapp.show()
    sys.exit(app.exec_())
