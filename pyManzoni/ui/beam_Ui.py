import sys
from PySide2 import QtCore
from PySide2.QtCore import QRect, Qt
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from georges_core import Distribution
from georges_core.units import ureg as _ureg
import plotly.express as px
import tempfile
import shutil


class BeamUi:

    def __init__(self, beam_layout):

        self.layout_beam = beam_layout
        self.beam = Distribution().from_5d_multigaussian_distribution(n=2)  # Default beam, 2 to avoid nan
        self.tmp_dir = tempfile.mkdtemp()
        self.plotwindows = None
        self.initialize_Ui()

    def initialize_Ui(self):

        # Create the table for kinematics
        self.horizontalLayout = QHBoxLayout()
        self.tableWidget = QTableWidget()
        self.horizontalLayout.addWidget(self.tableWidget)

        # Define the table widget
        self.tableWidget.setColumnCount(2)

        # Initialize the plot layout
        self.initialize_plot_layout()

        self.layout_beam.addLayout(self.horizontalLayout)
        self.tabWidget.setCurrentIndex(0)

        # Add button signal
        button_layout = QHBoxLayout()
        buttonBox = QDialogButtonBox()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_beam)
        plot_button = QPushButton("Generate plots")
        plot_button.clicked.connect(self.plot_beam)
        button_layout.addWidget(save_button)
        button_layout.addWidget(plot_button)
        button_layout.addWidget(buttonBox)
        self.layout_beam.addLayout(button_layout)

        # Initialize the table
        self.initialize_table()

    def initialize_table(self):

        # Add different possibilities to generate the beam
        self.beamtype = "Gaussian"
        self.change_beam()

        self.beam_list = QComboBox()
        self.beam_list.setObjectName(u"element_list")
        self.beam_list.addItems(["Gaussian"])
        self.beam_list.addItems(["Twiss"])
        self.beam_list.addItems(["Sigma-Matrix"])
        self.beam_list.addItems(["Userfile"])

        self.tableWidget.setCellWidget(0, 1, self.beam_list)
        self.beam_list.currentIndexChanged.connect(self.change_beam)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        self.update_table()
        self.tableWidget.itemChanged.connect(self.new_item)

    def initialize_plot_layout(self):
        # Define the tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName(u"tabWidget")

        # X-Y plane
        self.tab_xy = QWidget()
        self.tab_xy.setObjectName(u"tab_xy")
        self.XY_beam = QWebEngineView()
        self.XY_beam.setObjectName(u"XY_beam")
        self.tabWidget.addTab(self.XY_beam, "X - Y")

        # X - XP plane
        self.tab_xxp = QWidget()
        self.tab_xxp.setObjectName(u"tab_xxp")
        self.XPX_beam = QWebEngineView()
        self.XPX_beam.setObjectName(u"XPX_beam")
        self.tabWidget.addTab(self.XPX_beam, "X - PX")

        # Y - PY plane
        self.tab_yyp = QWidget()
        self.tab_yyp.setObjectName(u"tab_yyp")
        self.YPY_beam = QWebEngineView()
        self.YPY_beam.setObjectName(u"YPY_beam")
        self.tabWidget.addTab(self.YPY_beam, "Y - PY")

        # PX - PY plane
        self.tab_xpyp = QWidget()
        self.tab_xpyp.setObjectName(u"tab_xpyp")
        self.PXPY_beam = QWebEngineView()
        self.PXPY_beam.setObjectName(u"PXPY_beam")
        self.tabWidget.addTab(self.PXPY_beam, "PX - PY")

        # X - DPP plane
        self.tab_xdpp = QWidget()
        self.tab_xdpp.setObjectName(u"tab_xdpp")
        self.XDPP_beam = QWebEngineView()
        self.XDPP_beam.setObjectName(u"PXPY_beam")
        self.tabWidget.addTab(self.XDPP_beam, "X - DPP")

    def new_item(self):
        current_row = self.horizontalLayout.itemAt(0).widget().currentItem().row()
        if current_row != 0:
            new_value = float(self.tableWidget.item(current_row, 1).text())
            self.horizontalLayout.itemAt(0).widget().blockSignals(True)
            self.horizontalLayout.itemAt(0).widget().setItem(current_row, 1,
                                                             QTableWidgetItem('{:.3e}'.format(new_value)))
            self.set_beam()
            self.horizontalLayout.itemAt(0).widget().blockSignals(False)

    def change_beam(self):
        try:
            self.beamtype = self.beam_list.currentText()
        except AttributeError:
            pass
        finally:
            self.horizontalLayout.itemAt(0).widget().blockSignals(True)
            if self.beamtype == 'Gaussian' or self.beamtype == "Userfile":
                self.tableWidget.setRowCount(12)
                beam_dist_str = QTableWidgetItem("Beam type")  # From a Qscroll
                beam_dist_str.setFlags(Qt.ItemIsEnabled)
                n_part_str = QTableWidgetItem("N particles")
                n_part_str.setFlags(Qt.ItemIsEnabled)
                mean_x_str = QTableWidgetItem("Mean X (m)")
                mean_x_str.setFlags(Qt.ItemIsEnabled)
                mean_xp_str = QTableWidgetItem("Mean PX (rad)")
                mean_xp_str.setFlags(Qt.ItemIsEnabled)
                std_x_str = QTableWidgetItem("Std X (m)")
                std_x_str.setFlags(Qt.ItemIsEnabled)
                std_xp_str = QTableWidgetItem("Std PX (rad)")
                std_xp_str.setFlags(Qt.ItemIsEnabled)
                mean_y_str = QTableWidgetItem("Mean Y (m)")
                mean_y_str.setFlags(Qt.ItemIsEnabled)
                mean_yp_str = QTableWidgetItem("Mean PY (rad)")
                mean_yp_str.setFlags(Qt.ItemIsEnabled)
                std_y_str = QTableWidgetItem("Std Y (m)")
                std_y_str.setFlags(Qt.ItemIsEnabled)
                std_yp_str = QTableWidgetItem("Std PY (rad)")
                std_yp_str.setFlags(Qt.ItemIsEnabled)
                mean_dpp_str = QTableWidgetItem("Mean DPP (-)")
                mean_dpp_str.setFlags(Qt.ItemIsEnabled)
                std_dpp_str = QTableWidgetItem("Std DPP (-)")
                std_dpp_str.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(0, 0, beam_dist_str)
                self.tableWidget.setItem(1, 0, n_part_str)
                self.tableWidget.setItem(2, 0, mean_x_str)
                self.tableWidget.setItem(3, 0, mean_xp_str)
                self.tableWidget.setItem(4, 0, std_x_str)
                self.tableWidget.setItem(5, 0, std_xp_str)
                self.tableWidget.setItem(6, 0, mean_y_str)
                self.tableWidget.setItem(7, 0, mean_yp_str)
                self.tableWidget.setItem(8, 0, std_y_str)
                self.tableWidget.setItem(9, 0, std_yp_str)
                self.tableWidget.setItem(10, 0, mean_dpp_str)
                self.tableWidget.setItem(11, 0, std_dpp_str)

            if self.beamtype == 'Twiss':
                self.tableWidget.setRowCount(18)
                beam_dist_str = QTableWidgetItem("Beam type")  # From a Qscroll
                beam_dist_str.setFlags(Qt.ItemIsEnabled)
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
                std_dpp_str = QTableWidgetItem("Std DPP (-)")
                std_dpp_str.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(0, 0, beam_dist_str)
                self.tableWidget.setItem(1, 0, n_part_str)
                self.tableWidget.setItem(2, 0, mean_x_str)
                self.tableWidget.setItem(3, 0, mean_xp_str)
                self.tableWidget.setItem(4, 0, mean_y_str)
                self.tableWidget.setItem(5, 0, mean_yp_str)
                self.tableWidget.setItem(6, 0, mean_dpp_str)
                self.tableWidget.setItem(7, 0, beta_x_str)
                self.tableWidget.setItem(8, 0, alpha_x_str)
                self.tableWidget.setItem(9, 0, beta_y_str)
                self.tableWidget.setItem(10, 0, alpha_y_str)
                self.tableWidget.setItem(11, 0, emit_x_str)
                self.tableWidget.setItem(12, 0, emit_y_str)
                self.tableWidget.setItem(13, 0, dispx_str)
                self.tableWidget.setItem(14, 0, dispy_str)
                self.tableWidget.setItem(15, 0, disppx_str)
                self.tableWidget.setItem(16, 0, disppy_str)
                self.tableWidget.setItem(17, 0, std_dpp_str)

            self.horizontalLayout.itemAt(0).widget().blockSignals(False)
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.setItem(i, 1, None)

            self.set_beam()
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

    def set_beam(self):
        if self.beamtype == 'Gaussian':
            mean_val = self.beam.mean
            std_val = self.beam.std
            n = self.beam.n_particles if self.tableWidget.item(1, 1) is None else float(
                self.tableWidget.item(1, 1).text())
            x = mean_val['X'] if self.tableWidget.item(2, 1) is None else float(self.tableWidget.item(2, 1).text())
            px = mean_val['PX'] if self.tableWidget.item(3, 1) is None else float(self.tableWidget.item(3, 1).text())
            xrms = std_val['X'] if self.tableWidget.item(4, 1) is None else float(self.tableWidget.item(4, 1).text())
            pxrms = std_val['PX'] if self.tableWidget.item(5, 1) is None else float(self.tableWidget.item(5, 1).text())
            y = mean_val['Y'] if self.tableWidget.item(6, 1) is None else float(self.tableWidget.item(6, 1).text())
            py = mean_val['PY'] if self.tableWidget.item(7, 1) is None else float(self.tableWidget.item(7, 1).text())
            yrms = std_val['Y'] if self.tableWidget.item(8, 1) is None else float(self.tableWidget.item(8, 1).text())
            pyrms = std_val['PY'] if self.tableWidget.item(9, 1) is None else float(self.tableWidget.item(9, 1).text())
            dpp = mean_val['DPP'] if self.tableWidget.item(10, 1) is None else float(
                self.tableWidget.item(10, 1).text())
            dpprms = std_val['DPP'] if self.tableWidget.item(11, 1) is None else float(
                self.tableWidget.item(11, 1).text())

            self.beam = self.beam.from_5d_multigaussian_distribution(n=n,
                                                                     x=x * _ureg.m,
                                                                     px=px * _ureg.radians,
                                                                     xrms=xrms * _ureg.m,
                                                                     pxrms=pxrms * _ureg.radians,
                                                                     y=y * _ureg.m,
                                                                     py=py * _ureg.radians,
                                                                     yrms=yrms * _ureg.m,
                                                                     pyrms=pyrms * _ureg.radians,
                                                                     dpp=dpp,
                                                                     dpprms=dpprms
                                                                     )
        if self.beamtype == 'Twiss':
            mean_val = self.beam.mean
            n = self.beam.n_particles if self.tableWidget.item(1, 1) is None else float(
                self.tableWidget.item(1, 1).text())
            x = mean_val['X'] if self.tableWidget.item(2, 1) is None else float(self.tableWidget.item(2, 1).text())
            px = mean_val['PX'] if self.tableWidget.item(3, 1) is None else float(self.tableWidget.item(3, 1).text())
            y = mean_val['Y'] if self.tableWidget.item(4, 1) is None else float(self.tableWidget.item(4, 1).text())
            py = mean_val['PY'] if self.tableWidget.item(5, 1) is None else float(self.tableWidget.item(5, 1).text())
            dpp = mean_val['DPP'] if self.tableWidget.item(6, 1) is None else float(
                self.tableWidget.item(6, 1).text())
            betx = 1 if self.tableWidget.item(7, 1) is None else float(self.tableWidget.item(7, 1).text())
            alfx = 0 if self.tableWidget.item(8, 1) is None else float(self.tableWidget.item(8, 1).text())
            bety = 1 if self.tableWidget.item(9, 1) is None else float(self.tableWidget.item(9, 1).text())
            alfy = 0 if self.tableWidget.item(10, 1) is None else float(self.tableWidget.item(10, 1).text())
            emitx = 1e-9 if self.tableWidget.item(11, 1) is None else float(self.tableWidget.item(11, 1).text())
            emity = 1e-9 if self.tableWidget.item(12, 1) is None else float(self.tableWidget.item(12, 1).text())
            dispx = 0 if self.tableWidget.item(13, 1) is None else float(self.tableWidget.item(13, 1).text())
            dispy = 0 if self.tableWidget.item(14, 1) is None else float(self.tableWidget.item(14, 1).text())
            disppx = 0 if self.tableWidget.item(15, 1) is None else float(self.tableWidget.item(15, 1).text())
            disppy = 0 if self.tableWidget.item(16, 1) is None else float(self.tableWidget.item(16, 1).text())
            dpprms = 0 if self.tableWidget.item(17, 1) is None else float(self.tableWidget.item(17, 1).text())

            self.beam = self.beam.from_twiss_parameters(n=n,
                                                        x=x * _ureg.m,
                                                        px=px,
                                                        y=y * _ureg.m,
                                                        py=py,
                                                        dpp=dpp,
                                                        betax=betx * _ureg.m,
                                                        alphax=alfx,
                                                        betay=bety * _ureg.m,
                                                        alphay=alfy,
                                                        emitx=emitx * _ureg.m * _ureg.radians,
                                                        emity=emity * _ureg.m * _ureg.radians,
                                                        dispx=dispx * _ureg.m,
                                                        dispy=dispy * _ureg.m,
                                                        dispxp=disppx,
                                                        dispyp=disppy,
                                                        dpprms=dpprms)
        if self.beamtype == 'Sigma-Matrix':
            QMessageBox.information(QWidget(), "Info", "Sigma not yet implemented", QMessageBox.Ok)
        if self.beamtype == 'Userfile':
            # Load the beam
            df_beam, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv)")
            if df_beam:  # To avoid error if cancel is pressed
                self.beam.from_csv(path='.', filename=df_beam)

        self.update_table()

    def update_table(self):
        if self.beamtype == 'Gaussian' or self.beamtype == 'Userfile':
            self.horizontalLayout.itemAt(0).widget().blockSignals(True)
            mean_val = self.beam.mean
            std_val = self.beam.std
            self.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.beam.n_particles)))
            self.tableWidget.setItem(2, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['X']))))
            self.tableWidget.setItem(3, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['PX']))))
            self.tableWidget.setItem(4, 1, QTableWidgetItem(str('{:.3e}'.format(std_val['X']))))
            self.tableWidget.setItem(5, 1, QTableWidgetItem(str('{:.3e}'.format(std_val['PX']))))
            self.tableWidget.setItem(6, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['Y']))))
            self.tableWidget.setItem(7, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['PY']))))
            self.tableWidget.setItem(8, 1, QTableWidgetItem(str('{:.3e}'.format(std_val['Y']))))
            self.tableWidget.setItem(9, 1, QTableWidgetItem(str('{:.3e}'.format(std_val['PY']))))
            self.tableWidget.setItem(10, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['DPP']))))
            self.tableWidget.setItem(11, 1, QTableWidgetItem(str('{:.3e}'.format(std_val['DPP']))))
            self.horizontalLayout.itemAt(0).widget().blockSignals(False)

        if self.beamtype == 'Twiss':
            self.horizontalLayout.itemAt(0).widget().blockSignals(True)
            mean_val = self.beam.mean
            # I don't want to change the values dynamically
            betx = 1 if self.tableWidget.item(7, 1) is None else float(self.tableWidget.item(7, 1).text())
            alfx = 0 if self.tableWidget.item(8, 1) is None else float(self.tableWidget.item(8, 1).text())
            bety = 1 if self.tableWidget.item(9, 1) is None else float(self.tableWidget.item(9, 1).text())
            alfy = 0 if self.tableWidget.item(10, 1) is None else float(self.tableWidget.item(10, 1).text())
            emitx = 1e-9 if self.tableWidget.item(11, 1) is None else float(self.tableWidget.item(11, 1).text())
            emity = 1e-9 if self.tableWidget.item(12, 1) is None else float(self.tableWidget.item(12, 1).text())
            dispx = 0 if self.tableWidget.item(13, 1) is None else float(self.tableWidget.item(13, 1).text())
            dispy = 0 if self.tableWidget.item(14, 1) is None else float(self.tableWidget.item(14, 1).text())
            disppx = 0 if self.tableWidget.item(15, 1) is None else float(self.tableWidget.item(15, 1).text())
            disppy = 0 if self.tableWidget.item(16, 1) is None else float(self.tableWidget.item(16, 1).text())
            dpprms = 0 if self.tableWidget.item(17, 1) is None else float(self.tableWidget.item(17, 1).text())
            #
            self.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.beam.n_particles)))
            self.tableWidget.setItem(2, 1, QTableWidgetItem(str('{:3f}'.format(mean_val['X']))))
            self.tableWidget.setItem(3, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['PX']))))
            self.tableWidget.setItem(4, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['Y']))))
            self.tableWidget.setItem(5, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['PY']))))
            self.tableWidget.setItem(6, 1, QTableWidgetItem(str('{:.3e}'.format(mean_val['DPP']))))
            self.tableWidget.setItem(7, 1, QTableWidgetItem(str('{:.3e}'.format(betx))))
            self.tableWidget.setItem(8, 1, QTableWidgetItem(str('{:.3e}'.format(alfx))))
            self.tableWidget.setItem(9, 1, QTableWidgetItem(str('{:.3e}'.format(bety))))
            self.tableWidget.setItem(10, 1, QTableWidgetItem(str('{:.3e}'.format(alfy))))
            self.tableWidget.setItem(11, 1, QTableWidgetItem(str('{:.3e}'.format(emitx))))
            self.tableWidget.setItem(12, 1, QTableWidgetItem(str('{:.3e}'.format(emity))))
            self.tableWidget.setItem(13, 1, QTableWidgetItem(str('{:.3e}'.format(dispx))))
            self.tableWidget.setItem(14, 1, QTableWidgetItem(str('{:.3e}'.format(dispy))))
            self.tableWidget.setItem(15, 1, QTableWidgetItem(str('{:.3e}'.format(disppx))))
            self.tableWidget.setItem(16, 1, QTableWidgetItem(str('{:.3e}'.format(disppy))))
            self.tableWidget.setItem(17, 1, QTableWidgetItem(str('{:.3e}'.format(dpprms))))
            self.horizontalLayout.itemAt(0).widget().blockSignals(False)

    def save_beam(self):
        filename = QFileDialog.getSaveFileName(None, "Open File", "beam_distribution.csv", "CSV Files (*.csv)")
        if filename[0] != "":  # Cancel is not pressed
            self.beam.distribution.to_csv(filename[0], index=False)

    def plot_beam(self):
        # Initialize the plot layout
        self.plotwindows = QWidget()
        self.plotwindows.setGeometry(QRect(100, 100, 800, 800))

        plot_layout = QHBoxLayout(self.plotwindows)
        self.initialize_plot_layout()
        plot_layout.addWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(0)
        self.set_plot()
        self.plotwindows.show()

    def set_plot(self):
        template = {"layout": {"autosize": True,
                               'margin': dict(t=0, b=50, l=50, r=50),
                               }
                    }

        self.generate_plot(template, 'X', 'Y', 'x (m)', 'y (m)')
        self.generate_plot(template, 'X', 'PX', 'x (m)', 'xp (radians)')
        self.generate_plot(template, 'Y', 'PY', 'y (m)', 'yp (radians)')
        self.generate_plot(template, 'PX', 'PY', 'xp (radians)', 'yp (radians)')
        self.generate_plot(template, 'X', 'DPP', 'x (m)', 'dpp (-)')

        self.XY_beam.load(QtCore.QUrl().fromLocalFile(f"{self.tmp_dir}/distribution_XY.html"))

        self.XPX_beam.load(QtCore.QUrl().fromLocalFile(f"{self.tmp_dir}/distribution_XPX.html"))

        self.YPY_beam.load(QtCore.QUrl().fromLocalFile(f"{self.tmp_dir}/distribution_YPY.html"))

        self.PXPY_beam.load(QtCore.QUrl().fromLocalFile(f"{self.tmp_dir}/distribution_PXPY.html"))

        self.XDPP_beam.load(QtCore.QUrl().fromLocalFile(f"{self.tmp_dir}/distribution_XDPP.html"))

    def generate_plot(self, template, columns1, columns2, label1, label2):

        fig = px.density_heatmap(self.beam.distribution,
                                 x=self.beam.distribution[columns1],
                                 y=self.beam.distribution[columns2],
                                 nbinsx=50,
                                 nbinsy=50,
                                 marginal_x='histogram',
                                 marginal_y='histogram',
                                 width=600,
                                 height=600,
                                 template=template)
        fig.update_xaxes(title=label1)
        fig.write_html(f"{self.tmp_dir}/distribution_{columns1}{columns2}.html")

    def clean_tmp_files(self):
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    w = QMainWindow()
    beam_widget = QWidget()
    glw = QWidget(beam_widget)
    bl = QVBoxLayout(glw)
    bl.setContentsMargins(0, 0, 0, 0)
    form = Beam_Ui(bl)
    w.setLayout(form.layout_beam)
    w.setCentralWidget(glw)
    w.show()
    app.aboutToQuit.connect(form.clean_tmp_files)  # myExitHandler is a callable

    # Run the main Qt loop
    sys.exit(app.exec_())
