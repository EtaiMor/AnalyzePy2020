import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Cscan.CscanDocView import CscanDocView
from MainView import MainView
from GateDocView import GateDocView
from MyImageItem import MyImageItem

class CscanView(Dock):
    @staticmethod
    def init_instance(parent_view, gate_docview: GateDocView):
        t_min = int(gate_docview.getValues()[GateDocView.T_MIN_STR][0])
        t_max = int(gate_docview.getValues()[GateDocView.T_MAX_STR][0])
        c_scan = gate_docview.hdf_doc.get_c_scan(dn0=t_min, dn1=t_max)
        cscan_docview = CscanDocView(gate_docview, 'C-Scan', gate_docview.hdf_doc, c_scan)
        view = CscanView(parent_view, cscan_docview)
        return view

    def __init__(self, parent, cscan_docview: CscanDocView):
        super().__init__(cscan_docview.name(), closable=True)
        self.cscan_docview = cscan_docview
        self.gate_view = parent
        self.file_view = self.gate_view.parent
        self.main_view :MainView = self.file_view.parent

        image_item = MyImageItem(cscan_docview.c_scan)
        image_item.attach_mouseClickEvent(self.mouseClickEvent)
        self.image_view = pg.ImageView(self, cscan_docview.name(), imageItem=image_item)
        self.addWidget(self.image_view)
        self.main_view.dock_area.addDock(self, position='right')
        cscan_docview.slots.append(self.cscanChangedEvent)
        # self.cscan_docview.slots.append(self.cscanChangedEvent)

    def cscanChangedEvent(self, cscan):
        self.image_view.imageItem.setImage(cscan)


    def mouseClickEvent(self, event):
        i_indx = int(event.pos().y())
        j_indx = int(event.pos().x())
        gate_docview: GateDocView = self.cscan_docview.gate_docview
        gate_docview.update_ij_pos(i_indx, j_indx)


