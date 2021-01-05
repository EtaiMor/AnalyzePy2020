from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
# from GateDocView import GateDocView

class AscanDocView(pTypes.Parameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, a_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.a_scan = a_scan
        self.signal_ascanUpdatedEvent = None
        self.gate_docview = gate_docview
        self.gate_docview.ij_change_event_slots.append(self.on_update_ij_pos)
        self.ascan_changed_event_slots = list()

    def set_ascan(self, a_scan):
        self.a_scan = a_scan
        self.fire_ascan_changed_event(self.a_scan)

    def fire_ascan_changed_event(self, a_scan):
            for fun in self.ascan_changed_event_slots:
                fun(a_scan)

    def on_update_ij_pos(self, i_indx, j_indx):
        a_scan = self.hdf_doc.get_a_scan(i_indx, j_indx)
        self.set_ascan(a_scan)
