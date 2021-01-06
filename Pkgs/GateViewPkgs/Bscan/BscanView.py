import PyQt5.QtCore
import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Bscan.BscanDocView import BscanDocView
from GateDocView import GateDocView
from MainView import MainView
from MyImageItem import MyImageItem


class BscanView(Dock):
    @staticmethod
    def init_instance(parent_view, gate_docview: GateDocView):
        (num_wave, num_row, num_col, wave_len) = gate_docview.hdf_doc.get_data_dim()
        dn0, dn1 = gate_docview.get_dn_min_max()
        fwf_arr = gate_docview.get_fwf_arr()
        b_scan = gate_docview.hdf_doc.get_b_scan(int(num_row/2), None, dn0=dn0, dn1=dn1, fwf_arr = fwf_arr)
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
        self.set_popup_menu()
        self.main_view.dock_area.addDock(self, position='right')
        bscan_docview.bscan_changed_event += self.set_image_item

    def set_image_item(self, b_scan):
        if (self.bscan_docview.is_row):
            self.image_view.imageItem.setImage(b_scan.T)
        else:
            self.image_view.imageItem.setImage(b_scan)


    def mouseClickEvent(self, event):
        col_indx = int(event.pos().x())
        t_indx = int(event.pos().y())
        gate_docview: GateDocView = self.bscan_docview.gate_docview
        gate_docview.update_ij_pos(None, col_indx)

    def set_popup_menu(self):
        export_action = PyQt5.QtGui.QAction('check')
        self.image_view.scene.contextMenu.append(export_action)
        export_action.triggered.connect(self.check)

    def check(self):
        print('check')
