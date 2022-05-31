from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from georges_core import Kinematics, KinematicsException
from georges_core.units import ureg

ROW_TO_UNITS = {1: ureg.MeV,
                2: ureg.MeV / ureg.c,
                3: ureg.T * ureg.m,
                4: ureg.cm}


class KinematicUi:

    def __init__(self, kinematics_layout):

        self.layout_kin = kinematics_layout
        self.kinematics = None

        df_kinematics = self.get_df_kinematics()
        self.layout_kin.addWidget(df_kinematics)

    def new_item(self):
        current_row = self.layout_kin.itemAt(0).widget().currentItem().row()
        new_value = float(self.layout_kin.itemAt(0).widget().currentItem().text())
        new_kinematics = None
        try:
            new_kinematics = Kinematics(new_value * ROW_TO_UNITS[current_row])
            self.kinematics = new_kinematics

        except KinematicsException:
            self.error_layout("Invalid value encoutered in Kinematics")

        if new_kinematics:
            self.layout_kin.itemAt(0).widget().blockSignals(True)
            self.change_table_values(new_kinematics)
            self.layout_kin.itemAt(0).widget().blockSignals(False)

    def change_table_values(self, new_kinematics):
        df_kinematics = self.layout_kin.itemAt(0).widget()
        df_kinematics.setItem(1, 1, QTableWidgetItem('{:.3f}'.format(new_kinematics.ekin.m_as("MeV"))))
        df_kinematics.setItem(2, 1, QTableWidgetItem('{:.3f}'.format(new_kinematics.momentum.m_as("MeV/c"))))
        df_kinematics.setItem(3, 1, QTableWidgetItem('{:.3f}'.format(new_kinematics.brho.m_as("T m"))))
        df_kinematics.setItem(4, 1, QTableWidgetItem('{:.3f}'.format(new_kinematics.range.m_as("cm"))))
        df_kinematics.resizeColumnsToContents()
        df_kinematics.resizeRowsToContents()

    def get_df_kinematics(self):
        df_kinematics = QTableWidget()
        df_kinematics.setObjectName(u"df_kinematics")
        df_kinematics.setColumnCount(2)
        df_kinematics.setRowCount(5)

        particle_name_str = QTableWidgetItem("Particle")
        particle_name_val = QTableWidgetItem("Proton")
        kinetic_energy_str = QTableWidgetItem("Kinetic Energy (MeV)")
        momentum_str = QTableWidgetItem("Momentum (MeV/c)")
        brho_str = QTableWidgetItem("Brho (T.m)")
        range_str = QTableWidgetItem("Range (cm)")

        particle_name_str.setFlags(Qt.ItemIsEnabled)
        kinetic_energy_str.setFlags(Qt.ItemIsEnabled)
        momentum_str.setFlags(Qt.ItemIsEnabled)
        brho_str.setFlags(Qt.ItemIsEnabled)
        range_str.setFlags(Qt.ItemIsEnabled)
        particle_name_val.setFlags(Qt.ItemIsEnabled)

        df_kinematics.setItem(0, 0, particle_name_str)
        df_kinematics.setItem(1, 0, kinetic_energy_str)
        df_kinematics.setItem(2, 0, momentum_str)
        df_kinematics.setItem(3, 0, brho_str)
        df_kinematics.setItem(4, 0, range_str)
        df_kinematics.setItem(0, 1, particle_name_val)

        df_kinematics.itemChanged.connect(self.new_item)
        df_kinematics.resizeColumnsToContents()
        df_kinematics.resizeRowsToContents()
        return df_kinematics

    def error_layout(self, message):
        QMessageBox.warning(self, "Error", message, QMessageBox.Ok)
