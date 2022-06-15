import shutil
import sys
import logging
import tempfile
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox
from ui.pyManzoni_MainUi import MainWindow
from tracker import Tracker


class PyManzoni(MainWindow):

    def __init__(self):

        # Create a temporary directory
        self.tmp_folder = tempfile.TemporaryDirectory()
        self.tmp_folder_name = self.tmp_folder.name

        self.ui = super().__init__(tmp_folder=self.tmp_folder_name)
        self.tracker = Tracker(layout_results=self.layout_widget,
                               layout_sequence=self.s_ui,
                               tmp_folder=self.tmp_folder_name)

        # Connect buttons and actions
        self.connect_shortcut()
        self.connect_button()

    def connect_shortcut(self):
        self.menu_bar.trackAction.triggered.connect(self.track)
        self.menu_bar.loadAction.triggered.connect(self.tracker.layout_sequence.load_sequence)
        self.menu_bar.saveAction.triggered.connect(self.tracker.save_observer_data)

    def connect_button(self):
        self.tracking_button.setCheckable(True)
        self.tracking_button.toggle()
        self.tracking_button.clicked.connect(self.track)

        self.layout_widget.main_window.save_plot.clicked.connect(self.tracker.save_observer_data)

    def track(self):
        self.tracker(sequence=self.s_ui.sequence, beam=self.b_ui.beam, kinematics=self.k_ui.kinematics)

    def closeEvent(self, event):
        print(event)
        msgbox = QMessageBox(QMessageBox.Warning,
                             "",
                             "Are you sure you want to quit ? ",
                             buttons=QMessageBox.No | QMessageBox.Yes,
                             parent=self)
        msgbox.setDefaultButton(QMessageBox.No)
        if msgbox.exec_() == QMessageBox.Yes:
            logging.info(f"Clean up folder {self.tmp_folder_name}")
            shutil.rmtree(self.tmp_folder_name)
            app.quit()
            event.accept()  # let the window close
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = PyManzoni()
    myapp.show()
    app.aboutToQuit.connect(lambda: myapp.closeEvent)  # FIXME Gives a type error because event is not defined
    sys.exit(app.exec_())
