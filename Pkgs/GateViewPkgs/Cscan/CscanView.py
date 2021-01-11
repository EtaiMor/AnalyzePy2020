from PyQt5.QtWidgets import QStatusBar
import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Cscan.CscanDocView import CscanDocView
from MainView import MainView
from GateDocView import GateDocView
from MyImageItem import MyImageItem

class CscanView(Dock):
    @staticmethod
    def init_instance(gate_docview: GateDocView):
        fwf_arr = gate_docview.get_fwf_arr()
        dn0, dn1 = gate_docview.get_dn_min_max()
        c_scan = gate_docview.hdf_doc.get_c_scan(dn0=dn0, dn1=dn1, fwf_arr=fwf_arr)
        cscan_docview = CscanDocView(gate_docview, 'C-Scan', gate_docview.hdf_doc, c_scan)
        view = CscanView(cscan_docview)
        return view

    def __init__(self, cscan_docview: CscanDocView):
        super().__init__(cscan_docview.name(), closable=True)
        self.cscan_docview = cscan_docview
        self.gate_docview: GateDocView = cscan_docview.gate_docview

        image_item = MyImageItem(cscan_docview.c_scan)
        image_item.attach_mouseClickEvent(self.mouseClickEvent)

        self.image_view = pg.ImageView(self, cscan_docview.name(), imageItem=image_item)
        self.image_view.scene.sigMouseMoved.connect(self.mouseMoved)
        self.addWidget(self.image_view)

        cscan_docview.cscan_changed_event += self.set_image_item

    def set_image_item(self, cscan):
        self.image_view.imageItem.setImage(cscan)

    def mouseClickEvent(self, event):
        i_indx = int(event.pos().y())
        j_indx = int(event.pos().x())
        gate_docview: GateDocView = self.cscan_docview.gate_docview
        gate_docview.update_ij_pos(i_indx, j_indx)

    def mouseMoved(self, viewPos):
        image_item : MyImageItem = self.image_view.getImageItem()
        num_row = image_item.height()
        num_col = image_item.width()
        scenePos = self.image_view.getImageItem().mapFromScene(viewPos)
        row, col = int(scenePos.y()), int(scenePos.x())
        if (0 <= row < num_row) and (0 <= col < num_col):
            pos_str = self.cscan_docview.get_pos_string(row, col)
        else:
            pos_str = ''

        # self.parent_view.statusBar().showMessage(pos_str)
        # pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        # if p1.sceneBoundingRect().contains(pos):
        #     mousePoint = vb.mapSceneToView(pos)
        #     index = int(mousePoint.x())
        #     if index > 0 and index < len(data1):
        #         label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
        #     vLine.setPos(mousePoint.x())
        #     hLine.setPos(mousePoint.y())


