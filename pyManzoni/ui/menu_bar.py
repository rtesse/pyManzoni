from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon


class MenuBar:
    def __init__(self, main_window: QMainWindow = None):
        """
        Create the menu bar for the main window.
        Args:
            main_window ():
        """
        self.mainMenu = main_window.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")
        viewMenu = self.mainMenu.addMenu("View")
        editMenu = self.mainMenu.addMenu("Edit")
        searchMenu = self.mainMenu.addMenu("Font")
        helpMenu = self.mainMenu.addMenu("Help")

        self.create_menu_file()

    def create_menu_file(self):
        self.openAction = QAction(QIcon(), u"Open", self.mainMenu)
        self.openAction.setShortcut("Ctrl+O")

        self.saveAction = QAction(QIcon(), u"Save", self.mainMenu)
        self.saveAction.setShortcut("Ctrl+S")

        self.exitAction = QAction(QIcon(), u"Close", self.mainMenu)
        self.exitAction.setShortcut("Ctrl+X")

        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.exitAction)
