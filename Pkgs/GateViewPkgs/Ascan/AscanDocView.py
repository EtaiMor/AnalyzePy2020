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
        self.gate_docview.ij_change_event_slots.append(self.update_ascan)
        self.slots = list()

    def update_ascan(self, i_indx, j_indx):
        self.a_scan = self.hdf_doc.get_a_scan(i_indx, j_indx)
        self.update_all_slots()

    def update_all_slots(self):
        for fun in self.slots:
            fun(self.a_scan)
