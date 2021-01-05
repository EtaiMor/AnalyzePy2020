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
        self.bscan_changed_event_slots = list()

    def fire_bscan_changed_event(self, b_scan):
        for fun in self.bscan_changed_event_slots:
            fun(b_scan)

    def set_bscan(self, b_scan):
        self.b_scan = b_scan
        self.fire_bscan_changed_event(self.b_scan)

    def on_update_ij_pos(self, i_indx, j_indx):
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        b_scan = self.hdf_doc.get_b_scan(i_indx, None, dn0=t_min, dn1=t_max)
        self.set_bscan(b_scan)

    def on_update_time_range(self, t_min, t_max):
        row = self.gate_docview.get_ipos_param().value()
        b_scan = self.hdf_doc.get_b_scan(row, None, dn0=t_min, dn1=t_max)
        self.set_bscan(b_scan)

