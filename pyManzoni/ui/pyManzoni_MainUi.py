import sys

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow

from .menu_bar import MenuBar
from .layout_widgets import LayoutWidgets
from .kinematics_Ui import KinematicUi
from .beam_Ui import BeamUi
from .sequence_ui import SequenceUi

minimum_height = 700
minimum_width = 800


class MainWindow(QMainWindow):

    def __init__(self, tmp_folder: str):
        super().__init__()

        self.setWindowTitle("PyManzoni")
        self.setMinimumSize(QSize(minimum_width, minimum_height))

        # Create the menu bar
        self.menu_bar = MenuBar(self)

        # Create the layouts for line, samplers and beam properties
        self.layout_widget = LayoutWidgets(self, minimum_height, minimum_width)

        # Create the kinematics UI and add to kinematics layout.
        self.k_ui = KinematicUi(self.kinematics_layout)

        # Create the beam UI and add to beam properties.
        self.b_ui = BeamUi(self.beam_layout, tmp_folder)

        # Create the sequence UI
        self.s_ui = SequenceUi(self.sequence_layout, self.element_list)

    @property
    def tracking_button(self):
        return self.s_ui.track_sequence_button


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Define the main window
    window = MainWindow()
    window.show()

    app.aboutToQuit.connect(window.b_ui.clean_tmp_files)
    app.exec_()
