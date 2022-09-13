import os
import shutil

import georges
import georges_core
import pandas as _pd
import plotly.express as px
from georges import manzoni
from georges.manzoni import Beam
from georges.vis import ManzoniPlotlyArtist
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget


class Tracker(object):
    def __init__(
        self,
        layout_results=None,
        layout_sequence=None,
        tmp_folder: str = None,
    ):
        self.layout_results = layout_results
        self.layout_sequence = layout_sequence
        self.tmp_folder = tmp_folder
        self.tab3d = None
        self.manzoni_input = None
        self.has_run = False
        self.layout_results.main_window.element_list.activated.connect(
            self.set_plotting_element,
        )

    def __call__(self, sequence=None, beam=None, kinematics=None):

        if kinematics is None:
            QMessageBox.warning(
                QWidget(),
                "Warning",
                "No kinematics defined",
                QMessageBox.Ok,
            )
        else:
            self.prepare_sequence(sequence)
            if self.manzoni_input:
                self.sigma_observer = georges.manzoni.SigmaObserver()
                self.beam_observer = georges.manzoni.BeamObserver()
                self.manzoni_input.freeze()
                self.manzoni_input.track(
                    beam=Beam(kinematics=kinematics, distribution=beam.distribution),
                    observers=[self.sigma_observer, self.beam_observer],
                )

                self.plot_sigma_observer()
                self.fill_beam_observer()
                self.has_run = True

    def plot_sigma_observer(self):
        # generate the plot and save it
        artist = ManzoniPlotlyArtist(
            width=0.9 * self.layout_results.dock_widget_line.width(),
            height=0.8 * self.layout_results.dock_widget_line.height(),
        )
        artist.fig["autosize"] = True
        artist.tracking(self.sigma_observer, plane="both")
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self.tmp_folder, "tracking_XY_planes.html"))
        self.layout_results.main_window.XYplane_view.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "tracking_XY_planes.html"),
            ),
        )

        artist = ManzoniPlotlyArtist(
            width=0.9 * self.layout_results.dock_widget_line.width(),
            height=0.8 * self.layout_results.dock_widget_line.height(),
        )
        artist.tracking(self.sigma_observer, plane="X")
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self.tmp_folder, "tracking_X_plane.html"))
        self.layout_results.main_window.Xplane_view.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "tracking_X_plane.html"),
            ),
        )

        artist = ManzoniPlotlyArtist(
            width=0.9 * self.layout_results.dock_widget_line.width(),
            height=0.8 * self.layout_results.dock_widget_line.height(),
        )
        artist.tracking(self.sigma_observer, plane="Y")
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self.tmp_folder, "tracking_Y_plane.html"))
        self.layout_results.main_window.Yplane_view.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "tracking_Y_plane.html"),
            ),
        )

        self.layout_results.main_window.line_view.load(
            QtCore.QUrl().fromLocalFile(
                os.path.split(os.path.abspath(__file__))[0] + r"/test.html",
            ),
        )

    def set_plotting_element(self):
        if self.has_run:
            self.fill_beam_observer()

    def save_observer_data(self):
        if self.has_run:
            filenames = [
                "tracking_XY_planes.html",
                "tracking_X_plane.html",
                "tracking_Y_plane.html",
                "observer_X_Y.html",
                "observer_X_XP.html",
                "observer_Y_YP.html",
                "observer_X_DPP.html",
            ]
            folderpath = QFileDialog.getExistingDirectory()
            for f in filenames:
                shutil.copy(
                    os.path.join(self.tmp_folder, f),
                    os.path.join(folderpath, f),
                )

        else:
            QMessageBox.warning(
                QWidget(),
                "Warning",
                "No tracking performed",
                QMessageBox.Ok,
            )

    def fill_beam_observer(self):
        data_observer = self.beam_observer.to_df().loc[str(self.layout_sequence.element_list.currentText())]
        # artist = ManzoniPlotlyArtist(layout={"autosize": True,
        #                                      'margin': dict(t=0, b=50, l=50, r=50)})

        fig = px.density_heatmap(
            data_observer,
            x=data_observer["BEAM_OUT"][:, 0],
            y=data_observer["BEAM_OUT"][:, 2],
            nbinsx=50,
            nbinsy=50,
            marginal_x="histogram",
            marginal_y="histogram",
            width=600,
            height=600,
        )
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self.tmp_folder, "observer_X_Y.html"))
        self.layout_results.main_window.XY_histos.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "observer_X_Y.html"),
            ),
        )

        fig = px.density_heatmap(
            data_observer,
            x=data_observer["BEAM_OUT"][:, 0],
            y=data_observer["BEAM_OUT"][:, 1],
            nbinsx=50,
            nbinsy=50,
            marginal_x="histogram",
            marginal_y="histogram",
            width=600,
            height=600,
        )
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self.tmp_folder, "observer_X_XP.html"))
        self.layout_results.main_window.XXP_histo.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "observer_X_XP.html"),
            ),
        )

        fig = px.density_heatmap(
            data_observer,
            x=data_observer["BEAM_OUT"][:, 2],
            y=data_observer["BEAM_OUT"][:, 3],
            nbinsx=50,
            nbinsy=50,
            marginal_x="histogram",
            marginal_y="histogram",
            width=600,
            height=600,
        )
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self.tmp_folder, "observer_Y_YP.html"))
        self.layout_results.main_window.YYP_histo.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "observer_Y_YP.html"),
            ),
        )

        fig = px.density_heatmap(
            data_observer,
            x=data_observer["BEAM_OUT"][:, 0],
            y=data_observer["BEAM_OUT"][:, 4],
            nbinsx=50,
            nbinsy=50,
            marginal_x="histogram",
            marginal_y="histogram",
            width=600,
            height=600,
        )
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self.tmp_folder, "observer_X_DPP.html"))
        self.layout_results.main_window.XDPP_histo.load(
            QtCore.QUrl().fromLocalFile(
                os.path.join(self.tmp_folder, "observer_X_DPP.html"),
            ),
        )

        # Fill table
        distribution = georges_core.Distribution(
            distribution=_pd.DataFrame(
                data={
                    "X": data_observer["BEAM_OUT"][:, 0],
                    "PX": data_observer["BEAM_OUT"][:, 1],
                    "Y": data_observer["BEAM_OUT"][:, 2],
                    "PY": data_observer["BEAM_OUT"][:, 3],
                    "DPP": data_observer["BEAM_OUT"][:, 4],
                },
            ),
        )
        self.fill_table(distribution)

    def fill_table(self, distribution):
        mean_distribution = distribution.mean
        std_distribution = distribution.std
        try:
            tws_distribution = distribution.twiss
        except ZeroDivisionError:
            tws_distribution = {
                "emit_x": 0,
                "beta_x": 0,
                "alpha_x": 0,
                "disp_x": 0,
                "disp_xp": 0,
                "emit_y": 0,
                "beta_y": 0,
                "alpha_y": 0,
                "disp_y": 0,
                "disp_yp": 0,
            }

        n_part_str = QTableWidgetItem(f"{distribution.n_particles}")
        n_part_str.setFlags(Qt.ItemIsEnabled)
        mean_x_str = QTableWidgetItem(f"{round(mean_distribution['X'],5)}")
        mean_x_str.setFlags(Qt.ItemIsEnabled)
        mean_xp_str = QTableWidgetItem(f"{round(mean_distribution['PX'],5)}")
        mean_xp_str.setFlags(Qt.ItemIsEnabled)
        mean_y_str = QTableWidgetItem(f"{round(mean_distribution['Y'],5)}")
        mean_y_str.setFlags(Qt.ItemIsEnabled)
        mean_yp_str = QTableWidgetItem(f"{round(mean_distribution['PY'],5)}")
        mean_yp_str.setFlags(Qt.ItemIsEnabled)
        mean_dpp_str = QTableWidgetItem(f"{round(mean_distribution['DPP'],5)}")
        mean_dpp_str.setFlags(Qt.ItemIsEnabled)
        std_x_str = QTableWidgetItem(f"{round(std_distribution['X'],5)}")
        std_x_str.setFlags(Qt.ItemIsEnabled)
        std_xp_str = QTableWidgetItem(f"{round(std_distribution['PX'],5)}")
        std_xp_str.setFlags(Qt.ItemIsEnabled)
        std_y_str = QTableWidgetItem(f"{round(std_distribution['Y'],5)}")
        std_y_str.setFlags(Qt.ItemIsEnabled)
        std_yp_str = QTableWidgetItem(f"{round(std_distribution['PY'],5)}")
        std_yp_str.setFlags(Qt.ItemIsEnabled)
        std_dpp_str = QTableWidgetItem(f"{round(std_distribution['DPP'],5)}")
        std_dpp_str.setFlags(Qt.ItemIsEnabled)
        beta_x_str = QTableWidgetItem(f"{round(tws_distribution['beta_x'],5)}")
        beta_x_str.setFlags(Qt.ItemIsEnabled)
        alpha_x_str = QTableWidgetItem(f"{round(tws_distribution['alpha_x'],5)}")
        alpha_x_str.setFlags(Qt.ItemIsEnabled)
        beta_y_str = QTableWidgetItem(f"{round(tws_distribution['beta_y'],5)}")
        beta_y_str.setFlags(Qt.ItemIsEnabled)
        alpha_y_str = QTableWidgetItem(f"{round(tws_distribution['alpha_y'],5)}")
        alpha_y_str.setFlags(Qt.ItemIsEnabled)
        emit_x_str = QTableWidgetItem(f"{round(tws_distribution['emit_x'],5)}")
        emit_x_str.setFlags(Qt.ItemIsEnabled)
        emit_y_str = QTableWidgetItem(f"{round(tws_distribution['emit_y'],5)}")
        emit_y_str.setFlags(Qt.ItemIsEnabled)
        dispx_str = QTableWidgetItem(f"{round(tws_distribution['disp_x'],5)}")
        dispx_str.setFlags(Qt.ItemIsEnabled)
        dispy_str = QTableWidgetItem(f"{round(tws_distribution['disp_y'],5)}")
        dispy_str.setFlags(Qt.ItemIsEnabled)
        disppx_str = QTableWidgetItem(f"{round(tws_distribution['disp_xp'],5)}")
        disppx_str.setFlags(Qt.ItemIsEnabled)
        disppy_str = QTableWidgetItem(f"{round(tws_distribution['disp_yp'],5)}")
        disppy_str.setFlags(Qt.ItemIsEnabled)

        self.layout_results.main_window.tab_samplers_data.setItem(0, 1, n_part_str)
        self.layout_results.main_window.tab_samplers_data.setItem(1, 1, mean_x_str)
        self.layout_results.main_window.tab_samplers_data.setItem(2, 1, mean_xp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(3, 1, mean_y_str)
        self.layout_results.main_window.tab_samplers_data.setItem(4, 1, mean_yp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(5, 1, mean_dpp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(6, 1, std_x_str)
        self.layout_results.main_window.tab_samplers_data.setItem(7, 1, std_xp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(8, 1, std_y_str)
        self.layout_results.main_window.tab_samplers_data.setItem(9, 1, std_yp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(10, 1, std_dpp_str)
        self.layout_results.main_window.tab_samplers_data.setItem(11, 1, beta_x_str)
        self.layout_results.main_window.tab_samplers_data.setItem(12, 1, alpha_x_str)
        self.layout_results.main_window.tab_samplers_data.setItem(13, 1, beta_y_str)
        self.layout_results.main_window.tab_samplers_data.setItem(14, 1, alpha_y_str)
        self.layout_results.main_window.tab_samplers_data.setItem(15, 1, emit_x_str)
        self.layout_results.main_window.tab_samplers_data.setItem(16, 1, emit_y_str)
        self.layout_results.main_window.tab_samplers_data.setItem(17, 1, dispx_str)
        self.layout_results.main_window.tab_samplers_data.setItem(18, 1, dispy_str)
        self.layout_results.main_window.tab_samplers_data.setItem(19, 1, disppx_str)
        self.layout_results.main_window.tab_samplers_data.setItem(20, 1, disppy_str)

    def prepare_sequence(self, sequence):
        # Get the table and put in a dataFrame.
        if sequence is None:
            QMessageBox.warning(
                QWidget(),
                "Warning",
                "No sequence loaded",
                QMessageBox.Ok,
            )
        else:  # Not empty dataframe
            self.manzoni_input = manzoni.Input.from_sequence(sequence=sequence)
