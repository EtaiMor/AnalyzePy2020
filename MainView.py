from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDockWidget
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.dockarea import *

from PyQt5 import QtGui
import pyqtgraph as pg
import os
from MainDocView import MainDocView
from FileView import FileView


class MainView(QMainWindow):
    def __init__(self, doc_view : MainDocView):
        super().__init__()
        pg.setConfigOptions(imageAxisOrder='row-major')

        self.main_docview = doc_view

        self.title = "Analyze-2020"
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)

        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtGui.QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.dock_area = DockArea(self)
        self.layout.addWidget(self.dock_area)

        self.tree_parameters_widget = ParameterTree(self, showHeader=False)
        self.tree_parameters_widget.setParameters(self.main_docview, showTop=False)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.menu_open_filename)
        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.menu_close_filename)
        self.setDockNestingEnabled(True)

        self.tree_dock = Dock('Tree Dock',self.dock_area, autoOrientation=False, hideTitle=True)
        self.tree_dock.addWidget(self.tree_parameters_widget)
        self.dock_area.addDock(self.tree_dock, 'left')

        self.showMaximized()
        self.file_view_arr = list()


    def on_view_param_update(self):
        print('update')


    def menu_open_filename(self):
        my_settings = QSettings()

        last_open_file = my_settings.value('LAST_OPEN_FILE')
        if (last_open_file is None):
            last_open_dir = os.curdir
        else:
            last_open_dir = os.path.dirname(os.path.abspath(last_open_file))
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Hdf File", last_open_dir,
                                                   "(*.hdf)")
        self.add_file_view(file_name)
        my_settings.setValue('LAST_OPEN_FILE', file_name)

    def add_file_view(self, file_name):
        (file_docview, is_new) = self.main_docview.open_file(file_name)
        if (is_new):
            file_view = FileView(self, file_docview)
            # self.dock_area.addDock(file_view)
            self.file_view_arr.append(file_view)

    def menu_close_filename(self):
        print('Close file')