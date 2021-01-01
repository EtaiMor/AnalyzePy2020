from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes

class AscanDocView(pTypes.Parameter):
    def __init__(self, gate_docview, name, a_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = gate_docview.hdf_doc
        self.a_scan = a_scan
        self.signal_ascanUpdatedEvent = None
        self.gate_docview = gate_docview

    def attach_ascanUpdatedEvent(self, event_func):
        self.signal_ascanUpdatedEvent = event_func

    def update_ascan(self, i_indx, j_indx):
        self.a_scan = self.hdf_doc.get_a_scan(i_indx, j_indx)
        self.signal_ascanUpdatedEvent(self.a_scan)