from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Vscan.VscanDocView import VscanDocView
from GateDocView import GateDocView
from mayavi import mlab
import numpy as np
class VscanView(Dock):
    @staticmethod
    def init_instance(gate_docview: GateDocView):
        fwf_arr = gate_docview.get_fwf_arr()
        dn0, dn1 = gate_docview.get_dn_min_max()
        v_scan = gate_docview.hdf_doc.get_volume_ascans(ascan_mat=None, dn0=dn0, dn1 = dn1, fwf_arr=fwf_arr)
        vscan_docview = VscanDocView(gate_docview, 'V-Scan', gate_docview.hdf_doc, v_scan)
        view = VscanView(vscan_docview)
        return view

    def __init__(self, vscan_docview: VscanDocView):
        super().__init__(vscan_docview.name(), closable=True)
        self.vscan_docview = vscan_docview
        self.gate_docview: GateDocView = vscan_docview.gate_docview
        self.scene = None

        # image_item = MyImageItem(cscan_docview.c_scan)
        # image_item.attach_mouseClickEvent(self.mouseClickEvent)

        # self.image_view = pg.ImageView(self, cscan_docview.name(), imageItem=image_item)
        # self.image_view.scene.sigMouseMoved.connect(self.mouseMoved)
        # self.addWidget(self.image_view)

        vscan_docview.vscan_changed_event += self.on_vscan_changed


    def on_vscan_changed(self, v_scan: np.ndarray):
        (num_row, num_col, wave_len) = v_scan.shape
        if (mlab.get_engine() is None):
            mlab.figure('Volume Scan')
            mlab.show()

        mlab.clf(self.scene)
        # mlab.contour3d(v_scan)
        mlab.volume_slice(v_scan)


    # def set_image_item(self, cscan):
    #     self.image_view.imageItem.setImage(cscan)

    # def mouseClickEvent(self, event):
    #     i_indx = int(event.pos().y())
    #     j_indx = int(event.pos().x())
    #     gate_docview: GateDocView = self.cscan_docview.gate_docview
    #     gate_docview.update_ij_pos(i_indx, j_indx)
    #
    # def mouseMoved(self, viewPos):
    #     scenePos = self.image_view.getImageItem().mapFromScene(viewPos)
    #     row, col = int(scenePos.y()), int(scenePos.x())
    #     self.cscan_docview.set_mouse_ij_pos(row, col)



