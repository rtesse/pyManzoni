from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView


class LayoutWidgets:
    def __init__(self, main_window: QMainWindow = None, minimum_width: int = 0, minimum_height: int = 0):
        self.main_window = main_window
        self.minimum_width = minimum_width
        self.minimum_height = minimum_height

        # Define the widget that will be used for signals and slots
        self.main_window.element_list = None
        self.main_window.XY_histos = None
        self.main_window.XXP_histo = None
        self.main_window.YYP_histo = None
        self.main_window.XDPP_histo = None
        self.main_window.tab_samplers_data = None

        self.main_window.XYplane_view = None
        self.main_window.Xplane_view = None
        self.main_window.Yplane_view = None
        self.main_window.line_view = None

        self.main_window.kinematics_layout = None
        self.main_window.beam_layout = None
        self.main_window.sequence_layout = None

        # Create the widgets
        self.create_sampler_widget()
        self.create_line_widget()
        self.create_properties_widget()
        
    def create_sampler_widget(self):
        centralwidget = QWidget(self.main_window)
        centralwidget.setObjectName(u"centralwidget")
        centralwidget.setMinimumSize(QSize(int(2 * self.minimum_width / 3), int(0.9 * self.minimum_height / 2)))
        vl = QVBoxLayout(centralwidget)
        vl.setObjectName(u"verticalLayout")
        lh1 = QHBoxLayout()
        lh1.setObjectName(u"layout_histograms")

        lh2 = QHBoxLayout()
        lh2.setObjectName(u"layout_histograms")

        self.main_window.element_list = QComboBox(centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_window.element_list.sizePolicy().hasHeightForWidth())
        self.main_window.element_list.setSizePolicy(sizePolicy)

        self.main_window.save_plot = QPushButton(u"Save")

        lh1.addWidget(QLabel(u"Element: "))
        lh1.addWidget(self.main_window.element_list)
        lh1.addWidget(self.main_window.save_plot)

        tab_histograms = QTabWidget(centralwidget)
        self.main_window.XY_histos = QWebEngineView()
        self.main_window.XXP_histo = QWebEngineView()
        self.main_window.YYP_histo = QWebEngineView()
        self.main_window.XDPP_histo = QWebEngineView()
        tab_histograms.addTab(self.main_window.XY_histos, "X - Y")
        tab_histograms.addTab(self.main_window.XXP_histo, "X - XP")
        tab_histograms.addTab(self.main_window.YYP_histo, "Y - YP")
        tab_histograms.addTab(self.main_window.XDPP_histo, "X - DPP")

        self.main_window.tab_samplers_data = QTableWidget()
        self.main_window.tab_samplers_data.setColumnCount(2)
        self.main_window.tab_samplers_data.setRowCount(18)
        self.fill_samplers_data()

        lh2.addWidget(tab_histograms)
        lh2.addWidget(self.main_window.tab_samplers_data)
        vl.addLayout(lh1)
        vl.addLayout(lh2)

        self.main_window.setCentralWidget(centralwidget)

    def fill_samplers_data(self):
        n_part_str = QTableWidgetItem("N particles")
        n_part_str.setFlags(Qt.ItemIsEnabled)
        mean_x_str = QTableWidgetItem("Mean X (m)")
        mean_x_str.setFlags(Qt.ItemIsEnabled)
        mean_xp_str = QTableWidgetItem("Mean PX")
        mean_xp_str.setFlags(Qt.ItemIsEnabled)
        mean_y_str = QTableWidgetItem("Mean Y (m)")
        mean_y_str.setFlags(Qt.ItemIsEnabled)
        mean_yp_str = QTableWidgetItem("Mean PY")
        mean_yp_str.setFlags(Qt.ItemIsEnabled)
        mean_dpp_str = QTableWidgetItem("Mean DPP (-)")
        mean_dpp_str.setFlags(Qt.ItemIsEnabled)
        std_x_str = QTableWidgetItem("Std X (m)")
        std_x_str.setFlags(Qt.ItemIsEnabled)
        std_xp_str = QTableWidgetItem("Std PX (rad)")
        std_xp_str.setFlags(Qt.ItemIsEnabled)
        std_y_str = QTableWidgetItem("Std Y (m)")
        std_y_str.setFlags(Qt.ItemIsEnabled)
        std_yp_str = QTableWidgetItem("Std PY (rad)")
        std_yp_str.setFlags(Qt.ItemIsEnabled)
        std_dpp_str = QTableWidgetItem("Std DPP (-)")
        std_dpp_str.setFlags(Qt.ItemIsEnabled)
        beta_x_str = QTableWidgetItem("beta X (m)")
        beta_x_str.setFlags(Qt.ItemIsEnabled)
        alpha_x_str = QTableWidgetItem("alpha X")
        alpha_x_str.setFlags(Qt.ItemIsEnabled)
        beta_y_str = QTableWidgetItem("beta Y (m)")
        beta_y_str.setFlags(Qt.ItemIsEnabled)
        alpha_y_str = QTableWidgetItem("alpha Y")
        alpha_y_str.setFlags(Qt.ItemIsEnabled)
        emit_x_str = QTableWidgetItem("emittance X (m.rad)")
        emit_x_str.setFlags(Qt.ItemIsEnabled)
        emit_y_str = QTableWidgetItem("emittance Y (m.rad)")
        emit_y_str.setFlags(Qt.ItemIsEnabled)
        dispx_str = QTableWidgetItem("dispersion X (m)")
        dispx_str.setFlags(Qt.ItemIsEnabled)
        dispy_str = QTableWidgetItem("dispersion Y (m)")
        dispy_str.setFlags(Qt.ItemIsEnabled)
        disppx_str = QTableWidgetItem("D' X")
        disppx_str.setFlags(Qt.ItemIsEnabled)
        disppy_str = QTableWidgetItem("D' Y")
        disppy_str.setFlags(Qt.ItemIsEnabled)
        self.main_window.tab_samplers_data.setItem(0, 0, n_part_str)
        self.main_window.tab_samplers_data.setItem(1, 0, mean_x_str)
        self.main_window.tab_samplers_data.setItem(2, 0, mean_xp_str)
        self.main_window.tab_samplers_data.setItem(3, 0, mean_y_str)
        self.main_window.tab_samplers_data.setItem(4, 0, mean_yp_str)
        self.main_window.tab_samplers_data.setItem(5, 0, mean_dpp_str)
        self.main_window.tab_samplers_data.setItem(6, 0, std_x_str)
        self.main_window.tab_samplers_data.setItem(7, 0, std_xp_str)
        self.main_window.tab_samplers_data.setItem(8, 0, std_y_str)
        self.main_window.tab_samplers_data.setItem(9, 0, std_yp_str)
        self.main_window.tab_samplers_data.setItem(10, 0, std_dpp_str)
        self.main_window.tab_samplers_data.setItem(11, 0, beta_x_str)
        self.main_window.tab_samplers_data.setItem(12, 0, alpha_x_str)
        self.main_window.tab_samplers_data.setItem(13, 0, beta_y_str)
        self.main_window.tab_samplers_data.setItem(14, 0, alpha_y_str)
        self.main_window.tab_samplers_data.setItem(15, 0, emit_x_str)
        self.main_window.tab_samplers_data.setItem(16, 0, emit_y_str)
        self.main_window.tab_samplers_data.setItem(17, 0, dispx_str)
        self.main_window.tab_samplers_data.setItem(18, 0, dispy_str)
        self.main_window.tab_samplers_data.setItem(19, 0, disppx_str)
        self.main_window.tab_samplers_data.setItem(20, 0, disppy_str)

    def create_line_widget(self):
        self.dock_widget_line = QDockWidget(self.main_window)
        self.dock_widget_line.setWindowTitle(u"Beamline")
        self.dock_widget_line.setMinimumSize(QSize(self.minimum_width, int(0.9 * self.minimum_height / 2)))
        self.dock_widget_line.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.dock_widget_line.sizePolicy().hasHeightForWidth())
        self.dock_widget_line.setSizePolicy(size_policy)
        self.dock_widget_line.setFloating(False)

        # Add tab to the dock widget.
        dock_widget_contents_line = QWidget()
        hl = QHBoxLayout(dock_widget_contents_line)
        hl.setObjectName(u"hl")
        wtab = QTabWidget(dock_widget_contents_line)
        wtab.setEnabled(True)
        wtab.setTabBarAutoHide(False)

        self.main_window.XYplane_view = QWebEngineView()
        self.main_window.Xplane_view = QWebEngineView()
        self.main_window.Yplane_view = QWebEngineView()
        self.main_window.line_view = QWebEngineView()

        wtab.addTab(self.main_window.XYplane_view, u"X-Y plane")
        wtab.addTab(self.main_window.Xplane_view, u"X plane")
        wtab.addTab(self.main_window.Yplane_view, u"Y plane")
        wtab.addTab(self.main_window.line_view, u"3D view")

        wtab.setTabEnabled(3, False)

        hl.addWidget(wtab)
        self.dock_widget_line.setWidget(dock_widget_contents_line)
        self.main_window.addDockWidget(Qt.TopDockWidgetArea, self.dock_widget_line)

    def create_properties_widget(self):
        dock_widget_properties = QDockWidget(self.main_window)
        dock_widget_properties.setWindowTitle(u"Properties")
        dock_widget_properties.setMinimumSize(QSize(int(self.minimum_width / 3), int(0.9 * self.minimum_height / 2)))
        dock_widget_properties.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dock_widget_properties.sizePolicy().hasHeightForWidth())
        dock_widget_properties.setSizePolicy(size_policy)
        dock_widget_properties.setFloating(False)

        dock_widget_contents_sequence = QWidget()
        gl = QGridLayout(dock_widget_contents_sequence)
        beam_properties = QTabWidget(dock_widget_contents_sequence)
        beam_properties.setEnabled(True)
        beam_properties.setTabBarAutoHide(False)

        # For kinematics
        kinematics_widget = QWidget()
        vl = QWidget(kinematics_widget)
        self.main_window.kinematics_layout = QVBoxLayout(vl)
        self.main_window.kinematics_layout.setContentsMargins(0, 0, 0, 0)

        # For beam
        beam_widget = QWidget()
        glw = QWidget(beam_widget)
        self.main_window.beam_layout = QVBoxLayout(glw)
        self.main_window.beam_layout.setContentsMargins(0, 0, 0, 0)

        # For sequence
        sequence_widget = QWidget()
        vlw = QWidget(sequence_widget)
        vlw.setGeometry(QRect(-1, -1, 381, 271))
        self.main_window.sequence_layout = QVBoxLayout(vlw)
        self.main_window.sequence_layout.setContentsMargins(0, 0, 0, 0)

        # Add tab
        beam_properties.addTab(kinematics_widget, u"Kinematics")
        beam_properties.addTab(beam_widget, "Beam distribution")
        beam_properties.addTab(sequence_widget, "Sequence")

        gl.addWidget(beam_properties, 0, 0, 1, 1)

        dock_widget_properties.setWidget(dock_widget_contents_sequence)
        self.main_window.addDockWidget(Qt.LeftDockWidgetArea, dock_widget_properties)
