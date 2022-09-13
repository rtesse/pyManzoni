import sys

import georges_core
from georges_core.sequences import SurveySequence
from georges_core.units import ureg as _ureg
from PySide2.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SequenceUi:
    def __init__(self, sequence_layout=None, element_list=None):

        self.layout_sequence = sequence_layout
        self.element_list = element_list
        self.initialize_Ui()
        self.sequence = None

    def initialize_Ui(self):
        self.sequence_tableWidget = QTableWidget()
        self.sequence_tableWidget.setColumnCount(2)

        self.layout_sequence.addWidget(self.sequence_tableWidget)

        # Add button signal
        button_layout = QHBoxLayout()
        buttonBox = QDialogButtonBox()
        self.load_sequence_button = QPushButton("Load")
        self.load_sequence_button.clicked.connect(self.load_sequence)
        self.track_sequence_button = QPushButton("Track")
        button_layout.addWidget(self.load_sequence_button)
        button_layout.addWidget(self.track_sequence_button)
        button_layout.addWidget(buttonBox)
        self.layout_sequence.addLayout(button_layout)

    def load_sequence(self):
        # TODO into the tracker module.
        # if self.kinematics is None:
        #     QMessageBox.information(QWidget(), "Info", "Please provide a kinematics", QMessageBox.Ok)
        # SequenceMetadata(kinematics=kinematics,
        #                  particle=kinematics.particule)

        # if self.kinematics is not None:
        if self.sequence is not None:  # disconnect the signal first.
            self.sequence_tableWidget.itemChanged.disconnect()

        df_filename, _ = QFileDialog.getOpenFileName(
            QWidget(),
            "Open File",
            "",
            "CSV Files (*.csv)",
        )

        if df_filename:  # To avoid error if cancel is pressed
            # Give a default kinematics, this will be overwritten before the tracking
            self.sequence = SurveySequence(
                filename=df_filename,
                kinematics=georges_core.Kinematics(230 * _ureg.MeV),
            )
            self.sequence.expand()
            self.fill_table()
            self.fill_combobox()
            self.sequence_tableWidget.itemChanged.connect(self.new_item)

    def fill_table(self):
        sequence_df = self.sequence.df.fillna(0)
        sequence_df.reset_index(inplace=True)

        self.sequence_tableWidget.setColumnCount(len(sequence_df.columns))
        self.sequence_tableWidget.setRowCount(len(sequence_df))
        self.sequence_tableWidget.setHorizontalHeaderLabels(list(sequence_df.columns))

        for i in range(len(sequence_df)):
            for j in range(len(sequence_df.columns)):
                try:
                    x = sequence_df.iloc[i, j]
                    if isinstance(x, list):
                        x = ["{:.3f}".format(t.magnitude) for t in x]
                        x = " ".join(map(str, x))
                    else:
                        x = "{:.3f}".format(x.magnitude)
                except BaseException:
                    x = sequence_df.iloc[i, j]
                if x:
                    self.sequence_tableWidget.setItem(i, j, QTableWidgetItem(x))
                else:
                    self.sequence_tableWidget.setItem(i, j, QTableWidgetItem("None"))

    def new_item(self):
        current_row = self.sequence_tableWidget.currentItem().row()
        current_column = self.sequence_tableWidget.currentItem().column()
        new_value = self.sequence_tableWidget.currentItem().text()
        self.sequence_tableWidget.blockSignals(True)
        self.sequence.df.iloc[current_row, current_column] = new_value
        self.fill_combobox()  # In case of the name of the element changed
        self.sequence_tableWidget.blockSignals(False)

    def fill_combobox(self):
        self.element_list.clear()
        self.element_list.addItems(self.sequence.df.index)


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    w = QMainWindow()
    beam_widget = QWidget()
    glw = QWidget(beam_widget)
    bl = QVBoxLayout(glw)
    bl.setContentsMargins(0, 0, 0, 0)
    form = SequenceUi(bl)
    w.setLayout(form.layout_sequence)
    w.setCentralWidget(glw)
    w.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
