import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from pyqtgraph.parametertree import types as pTypes

from CscanDocView import CscanDocView
from GateDocView import GateDocView
from MyImageItem import MyImageItem
import numpy as np

class CScanView(Dock):
    def __init__(self, parent, cscan_docview: CscanDocView):
        super().__init__(cscan_docview.name(), closable=True)
        self.cscan_docview = cscan_docview
        self.gate_view = parent
        self.file_view = self.gate_view.parent
        self.main_view = self.file_view.parent

        image_item = MyImageItem(cscan_docview.c_scan)
        image_item.attach_mouseClickEvent(self.mouseClickEvent)
        self.image_view = pg.ImageView(self, cscan_docview.name(), imageItem=image_item)
        self.addWidget(self.image_view)


    def mouseClickEvent(self, event):
        i_indx = int(event.pos().y())
        j_indx = int(event.pos().x())
        gate_docview: GateDocView = self.cscan_docview.gate_docview
        gate_docview.update_ij_pos(i_indx, j_indx)


