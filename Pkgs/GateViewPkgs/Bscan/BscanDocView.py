from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView
from Event import Event

# from GateDocView import GateDocView

class BscanDocView(pTypes.GroupParameter):
    ORIENTATION_STR = 'Orientation'

    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, b_scan, is_row, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.b_scan = b_scan
        self.is_row = is_row
        self.gate_docview: GateDocView = gate_docview
        self.gate_docview.ij_change_event += self.on_update_ij_pos
        self.gate_docview.t_range_event += self.on_update_time_range
        self.bscan_changed_event = Event()
        self.add_to_parent()


    def add_to_parent(self):
        self.gate_docview.addChild(self)
        self.AddChildWithSlot({'name': BscanDocView.ORIENTATION_STR, 'type': 'list',
                               'values': ['Horizontal', 'Vertical'], 'value': 'Horizontal'}, self.set_orientation)

    def set_orientation(self, changeDesc, orientation):
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        if (orientation is 'Horizontal'):
            self.is_row = True
            row = self.gate_docview.get_ipos_param().value()
            b_scan = self.hdf_doc.get_b_scan(row, None, dn0=t_min, dn1=t_max)
        else:
            self.is_row = False
            col = self.gate_docview.get_jpos_param().value()
            b_scan = self.hdf_doc.get_b_scan(None, col, dn0=t_min, dn1=t_max)

        self.set_bscan(b_scan)


    def AddChildWithSlot(self, dict, slot):
        child = self.addChild(dict)
        child.sigValueChanged.connect(slot)

    def set_bscan(self, b_scan):
        self.b_scan = b_scan
        self.bscan_changed_event(self.b_scan)

    def on_update_ij_pos(self, i_indx, j_indx):
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()

        if (self.is_row):
            b_scan = self.hdf_doc.get_b_scan(i_indx, None, dn0=t_min, dn1=t_max)
        else:
            b_scan = self.hdf_doc.get_b_scan(None, j_indx, dn0=t_min, dn1=t_max)
        self.set_bscan(b_scan)

    def on_update_time_range(self, t_min, t_max):
        if (self.is_row):
            row = self.gate_docview.get_ipos_param().value()
            b_scan = self.hdf_doc.get_b_scan(row, None, dn0=t_min, dn1=t_max)
        else:
            col = self.gate_docview.get_jpos_param().value()
            b_scan = self.hdf_doc.get_b_scan(None, col, dn0=t_min, dn1=t_max)
        self.set_bscan(b_scan)

