from PyQt5.QtWidgets import QDockWidget
from pyqtgraph.dockarea import Dock, DockArea

from FileDocView import FileDocView
from GateDocView import GateDocView
from GateView import GateView

class FileView(Dock):
    def __init__(self, parent, file_docview: FileDocView):
        super().__init__(file_docview.name())
        self.parent = parent
        self.file_docview = file_docview
        self.gate_view_arr = list()
        self.add_gate_view()

    def add_gate_view(self):
        gate_docview = self.file_docview.open_gate()
        gate_view = GateView(self, gate_docview)
        # self.dock_area.addDock(gate_view, 'right')
        self.gate_view_arr.append(gate_view)
        return gate_view

