from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
import GateDocView

class CscanDocView(pTypes.Parameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, c_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.c_scan = c_scan
        self.gate_docview: GateDocView.GateDocView = gate_docview
        self.gate_docview.addChild(self)
        self.slots = list()
        self.gate_docview.t_range_event_slots.append(self.update_cscan)

    def update_cscan(self, time_range):
        self.c_scan = self.hdf_doc.get_c_scan(dn0=time_range[0], dn1=time_range[1])
        self.update_all_slots()

    def update_all_slots(self):
        for fun in self.slots:
            fun(self.c_scan)

