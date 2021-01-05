import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Bscan.BscanDocView import BscanDocView
from GateDocView import GateDocView
from MainView import MainView
from MyImageItem import MyImageItem


class BscanView(Dock):
    @staticmethod
    def init_instance(parent_view, gate_docview: GateDocView):
        tmin = int(gate_docview.getValues()[GateDocView.T_MIN_STR][0])
        tmax = int(gate_docview.getValues()[GateDocView.T_MAX_STR][0])
        (num_wave, num_row, num_col, wave_len) = gate_docview.hdf_doc.get_data_dim()
        b_scan = gate_docview.hdf_doc.get_b_scan(int(num_row/2), None, dn0=tmin, dn1=tmax)
        bscan_docview = BscanDocView(gate_docview, 'B-Scan', gate_docview.hdf_doc, b_scan, True)
        view = BscanView(parent_view, bscan_docview)
        return view

    def __init__(self, gate_view, bscan_docview: BscanDocView):
        super().__init__(bscan_docview.name(), closable=True)
        self.bscan_docview = bscan_docview
        self.gate_docview: GateDocView = bscan_docview.gate_docview
        self.file_view = gate_view
        self.file_view = gate_view.parent
        self.main_view :MainView = self.file_view.parent

        image_item = MyImageItem(bscan_docview.b_scan.T)
        image_item.attach_mouseClickEvent(self.mouseClickEvent)
        self.image_view = pg.ImageView(self, bscan_docview.name(), imageItem=image_item)
        self.addWidget(self.image_view)
        self.main_view.dock_area.addDock(self, position='right')
        bscan_docview.bscan_changed_event_slots.append(self.set_image_item)

    def set_image_item(self, bscan):
        self.image_view.imageItem.setImage(bscan.T)

    def mouseClickEvent(self, event):
        col_indx = int(event.pos().x())
        t_indx = int(event.pos().y())
        gate_docview: GateDocView = self.bscan_docview.gate_docview
        gate_docview.update_ij_pos(None, col_indx)
