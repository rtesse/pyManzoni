"""
This file creates the menu bar and prepare all the button that will be connected in the main menu.

"""
import webbrowser
from PySide2.QtWidgets import QAction, QMainWindow
from PySide2.QtGui import QIcon


class MenuBar:

    def __init__(self, main_window: QMainWindow = None):
        """
        Create the menu bar for the main window.
        Args:
            main_window ():
        """
        self.mainMenu = main_window.menuBar()
        self.editMenu = self.mainMenu.addMenu("Edit")
        self.helpMenu = self.mainMenu.addMenu("Help")

        self.create_edit_menu_file()
        self.create_help_menu_file()

    def create_edit_menu_file(self):
        self.loadAction = QAction(QIcon(), u"Load", self.mainMenu)
        self.loadAction.setShortcut("Ctrl+L")

        self.trackAction = QAction(QIcon(), u"Track", self.mainMenu)
        self.trackAction.setShortcut("Ctrl+T")

        self.saveAction = QAction(QIcon(), u"Save", self.mainMenu)
        self.saveAction.setShortcut("Ctrl+S")

        self.editMenu.addAction(self.loadAction)
        self.editMenu.addAction(self.trackAction)
        self.editMenu.addAction(self.saveAction)

    @staticmethod
    def open_webbrowser(url: str = None):
        webbrowser.open(url)

    def create_help_menu_file(self):
        self.helpDocumentationMenu = self.helpMenu.addMenu("Documentation")
        self.helpManzoni = QAction(QIcon(), u"Manzoni", self.mainMenu)
        self.helpManzoni.triggered.connect(lambda _: self.open_webbrowser("https://ulb-metronu.github.io/georges/"))
        self.helpZgoubi = QAction(QIcon(), u"Zgoubi", self.mainMenu)
        self.helpZgoubi.triggered.connect(
            lambda _: self.open_webbrowser("https://sourceforge.net/projects/zgoubi/lists/zgoubi-svn"))

        self.helpDocumentationMenu.addAction(self.helpManzoni)
        self.helpDocumentationMenu.addAction(self.helpZgoubi)
