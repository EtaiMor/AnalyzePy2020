from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
import GateDocView
from Event import Event


class CscanDocView(pTypes.GroupParameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, c_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.c_scan = c_scan
        self.gate_docview: GateDocView.GateDocView = gate_docview
        self.gate_docview.t_range_event += self.on_update_time_range
        self.gate_docview.fwf_changed_event += self.on_update_fwf
        self.cscan_changed_event = Event()
        self.add_to_parent()

    def add_to_parent(self):
        self.gate_docview.addChild(self)

    def set_cscan(self):
        dn0, dn1 = self.gate_docview.get_dn_min_max()
        fwf_arr = self.gate_docview.get_fwf_arr()
        self.c_scan = self.hdf_doc.get_c_scan(dn0=dn0, dn1=dn1, fwf_arr=fwf_arr)
        self.cscan_changed_event(self.c_scan)

    def on_update_time_range(self):
        self.set_cscan()

    def on_update_fwf(self):
        self.set_cscan()

