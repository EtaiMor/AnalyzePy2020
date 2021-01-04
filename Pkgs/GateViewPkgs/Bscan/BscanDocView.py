from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView


# from GateDocView import GateDocView

class BscanDocView(pTypes.Parameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, b_scan, is_row, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.b_scan = b_scan
        self.is_row = is_row
        self.gate_docview: GateDocView = gate_docview
        self.gate_docview.ij_change_event_slots.append(self.on_update_ij_pos)
        self.gate_docview.t_range_event_slots.append(self.on_update_time_range)
        self.slots = list()

    def on_update_ij_pos(self, i_indx, j_indx):
        tmin = self.gate_docview.get_tmin_param().value()
        tmax = self.gate_docview.get_tmax_param().value()
        self.b_scan = self.hdf_doc.get_b_scan(i_indx, None, dn0=tmin, dn1=tmax)
        self.update_all_slots()

    def on_update_time_range(self, time_range):
        row = self.gate_docview.get_ipos_param().value()
        self.b_scan = self.hdf_doc.get_b_scan(row, None, dn0=time_range[0], dn1=time_range[1])
        self.update_all_slots()

    def update_all_slots(self):
        for fun in self.slots:
            fun(self.b_scan)
