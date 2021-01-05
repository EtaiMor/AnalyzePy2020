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
        self.gate_docview.t_range_event_slots.append(self.on_update_time_range)
        self.cscan_changed_event_slots = list()

    def set_cscan(self, t_min, t_max):
        self.c_scan = self.hdf_doc.get_c_scan(dn0=t_min, dn1=t_max)
        self.fire_cscan_changed_event(self.c_scan)

    def fire_cscan_changed_event(self, c_scan):
        for fun in self.cscan_changed_event_slots:
            fun(c_scan)


    def on_update_time_range(self, t_min, t_max):
        self.set_cscan(t_min, t_max)


