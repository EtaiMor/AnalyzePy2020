import PyQt5.QtCore
import pyqtgraph as pg
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Bscan.BscanDocView import BscanDocView
from GateDocView import GateDocView
from MainView import MainView
from MyImageItem import MyImageItem


class BscanView(Dock):


    @staticmethod
    def init_instance(gate_docview: GateDocView):
        (num_wave, num_row, num_col, wave_len) = gate_docview.hdf_doc.get_data_dim()
        dn0, dn1 = gate_docview.get_dn_min_max()
        fwf_arr = gate_docview.get_fwf_arr()
        b_scan = gate_docview.hdf_doc.get_b_scan(int(num_row/2), None, dn0=dn0, dn1=dn1, fwf_arr = fwf_arr)
        bscan_docview = BscanDocView(gate_docview, 'B-Scan', gate_docview.hdf_doc, b_scan, BscanDocView.HORIZONTAL_TXT)
        view = BscanView(bscan_docview)
        return view

    def __init__(self, bscan_docview: BscanDocView):
        super().__init__(bscan_docview.name(), closable=True)
        self.bscan_docview = bscan_docview
        self.gate_docview: GateDocView = bscan_docview.gate_docview

        image_item = MyImageItem(bscan_docview.b_scan.T)
        image_item.attach_mouseClickEvent(self.mouseClickEvent)
        self.image_view = pg.ImageView(self, bscan_docview.name(), imageItem=image_item)
        self.addWidget(self.image_view)
        self.set_popup_menu()
        bscan_docview.bscan_changed_event += self.set_image_item

    def set_image_item(self, b_scan):
        if (self.bscan_docview.orientation == BscanDocView.HORIZONTAL_TXT):
            self.image_view.imageItem.setImage(b_scan.T)
        else:
            self.image_view.imageItem.setImage(b_scan)


    def mouseClickEvent(self, event):
        col_indx = int(event.pos().x())
        t_indx = int(event.pos().y())
        gate_docview: GateDocView = self.bscan_docview.gate_docview
        gate_docview.update_ij_pos(None, col_indx)

    def set_popup_menu(self):
        b_scan_type_menu = QMenu(BscanDocView.ORIENTATION_STR, self)
        group = QActionGroup(b_scan_type_menu)
        for text in BscanDocView.ORIENTATION_LIST:
            action = QAction(text, b_scan_type_menu, checkable=True, checked= text == BscanDocView.HORIZONTAL_TXT)
            b_scan_type_menu.addAction(action)
            group.addAction(action)
        group.setExclusive(True)
        group.triggered.connect(self.on_bscan_type_triggered)
        self.image_view.scene.contextMenu.append(b_scan_type_menu)

    def on_bscan_type_triggered(self, action):
        # if (action.text() == BscanDocView.bscan_types_list[0]):
        #     print(BscanDocView.bscan_types_list[0])
        self.bscan_docview.set_orientation(action.text())

    def check(self):
        print('check')
