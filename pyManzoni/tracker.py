import tempfile
import os
from PySide2 import QtCore
from PySide2.QtWidgets import *
import plotly.express as px
import georges
from georges import manzoni
from georges.manzoni import Beam
from georges.vis import ManzoniPlotlyArtist


class Tracker(object):
    def __init__(self, layout_results=None, layout_sequence=None):
        self.layout_results = layout_results
        self.layout_sequence = layout_sequence
        self.tab3d = None
        self._path = tempfile.TemporaryDirectory()
        self.manzoni_input = None
        self.has_run = False

    def __call__(self, sequence=None, beam=None, kinematics=None):

        if kinematics is None:
            QMessageBox.warning(QWidget(), "Warning", "No kinematics defined", QMessageBox.Ok)
        else:
            self.prepare_sequence(sequence)
            if self.manzoni_input:
                self.sigma_observer = georges.manzoni.SigmaObserver()
                self.beam_observer = georges.manzoni.BeamObserver()
                self.manzoni_input.freeze()
                self.manzoni_input.track(beam=Beam(kinematics=kinematics,
                                                   distribution=beam.distribution),
                                         observers=[self.sigma_observer, self.beam_observer])

                self.plot_sigma_observer()
                self.plot_beam_observer()
                self.has_run = True

    def plot_sigma_observer(self):
        # generate the plot and save it
        artist = ManzoniPlotlyArtist(width=0.9 * self.layout_results.dock_widget_line.width(),
                                     height=0.8 * self.layout_results.dock_widget_line.height())
        artist.fig['autosize'] = True
        artist.tracking(self.sigma_observer, plane='both')
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self._path.name, "tracking_both_planes.html"))
        self.layout_results.main_window.XYplane_view.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "tracking_both_planes.html")))

        artist = ManzoniPlotlyArtist(width=0.9 * self.layout_results.dock_widget_line.width(),
                                     height=0.8 * self.layout_results.dock_widget_line.height())
        artist.tracking(self.sigma_observer, plane='X')
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self._path.name, "tracking_X_plane.html"))
        self.layout_results.main_window.Xplane_view.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "tracking_X_plane.html")))

        artist = ManzoniPlotlyArtist(width=0.9 * self.layout_results.dock_widget_line.width(),
                                     height=0.8 * self.layout_results.dock_widget_line.height())
        artist.tracking(self.sigma_observer, plane='Y')
        artist.plot_cartouche(self.layout_sequence.sequence.df, vertical_position=1.15)
        artist.save_html(os.path.join(self._path.name, "tracking_Y_plane.html"))
        self.layout_results.main_window.Yplane_view.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "tracking_Y_plane.html")))

        self.layout_results.main_window.line_view.load(QtCore.QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r'/test.html'))

    def set_plotting_element(self):
        if self.has_run:
            self.plot_beam_observer()

    def plot_beam_observer(self):
        data_observer = self.beam_observer.to_df().loc[str(self.layout_sequence.element_list.currentText())]
        # artist = ManzoniPlotlyArtist(layout={"autosize": True,
        #                                      'margin': dict(t=0, b=50, l=50, r=50)})

        fig = px.density_heatmap(data_observer,
                                 x=data_observer['BEAM_OUT'][:, 0],
                                 y=data_observer['BEAM_OUT'][:, 2],
                                 nbinsx=50,
                                 nbinsy=50,
                                 marginal_x='histogram',
                                 marginal_y='histogram',
                                 width=600,
                                 height=600)
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self._path.name, "observer_X_Y.html"))
        self.layout_results.main_window.XY_histos.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "observer_X_Y.html")))

        fig = px.density_heatmap(data_observer,
                                 x=data_observer['BEAM_OUT'][:, 0],
                                 y=data_observer['BEAM_OUT'][:, 1],
                                 nbinsx=50,
                                 nbinsy=50,
                                 marginal_x='histogram',
                                 marginal_y='histogram',
                                 width=600,
                                 height=600)
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self._path.name, "observer_X_XP.html"))
        self.layout_results.main_window.XXP_histo.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "observer_X_XP.html")))

        fig = px.density_heatmap(data_observer,
                                 x=data_observer['BEAM_OUT'][:, 2],
                                 y=data_observer['BEAM_OUT'][:, 3],
                                 nbinsx=50,
                                 nbinsy=50,
                                 marginal_x='histogram',
                                 marginal_y='histogram',
                                 width=600,
                                 height=600)
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self._path.name, "observer_Y_YP.html"))
        self.layout_results.main_window.YYP_histo.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "observer_Y_YP.html")))

        fig = px.density_heatmap(data_observer,
                                 x=data_observer['BEAM_OUT'][:, 0],
                                 y=data_observer['BEAM_OUT'][:, 4],
                                 nbinsx=50,
                                 nbinsy=50,
                                 marginal_x='histogram',
                                 marginal_y='histogram',
                                 width=600,
                                 height=600)
        # fig.update_xaxes(title=label1)
        fig.write_html(os.path.join(self._path.name, "observer_X_DPP.html"))
        self.layout_results.main_window.XDPP_histo.load(
            QtCore.QUrl().fromLocalFile(os.path.join(self._path.name, "observer_X_DPP.html")))

    def prepare_sequence(self, sequence):
        # Get the table and put in a dataFrame.
        if sequence is None:
            QMessageBox.warning(QWidget(), "Warning", "No sequence loaded", QMessageBox.Ok)
        else:  # Not empty dataframe
            self.manzoni_input = manzoni.Input.from_sequence(sequence=sequence)
