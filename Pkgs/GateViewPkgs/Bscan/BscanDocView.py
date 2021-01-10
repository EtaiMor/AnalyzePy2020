from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView, MyGroupParameter
from Event import Event

# from GateDocView import GateDocView

class BscanDocView(MyGroupParameter):
    ORIENTATION_STR = 'Orientation'
    HORIZONTAL_TXT = 'Horizontal'
    VERTICAL_TXT = 'Vertical'
    ORIENTATION_LIST = (HORIZONTAL_TXT, VERTICAL_TXT)

    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, b_scan, orientation, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.b_scan = b_scan
        self.orientation = orientation
        self.gate_docview: GateDocView = gate_docview
        self.gate_docview.ij_change_event += self.on_update_ij_pos
        self.gate_docview.t_range_event += self.on_update_time_range
        self.gate_docview.fwf_changed_event += self.on_update_fwf
        self.bscan_changed_event = Event()
        # self.add_to_parent()


    # def add_to_parent(self):
    #     self.gate_docview.addChild(self)
    #     self.AddChildWithSlot({'name': BscanDocView.ORIENTATION_STR, 'type': 'list',
    #                            'values': ['Horizontal', 'Vertical'], 'value': 'Horizontal'}, self.set_orientation)

    # def get_orientation(self):
    #     return self.get_value_by_name(BscanDocView.ORIENTATION_STR)
    def set_orientation(self, orientation):
        if (self.orientation != orientation):
            self.orientation = orientation
            self.set_bscan()

    def set_bscan(self):
        dn_0, dn_1 = self.gate_docview.get_dn_min_max()
        fwf_arr = self.gate_docview.get_fwf_arr()

        if (self.orientation == BscanDocView.HORIZONTAL_TXT):
            row = self.gate_docview.get_ipos_param().value()
            self.b_scan = self.hdf_doc.get_b_scan(row, None, dn0=dn_0, dn1=dn_1, fwf_arr=fwf_arr)
        else:
            col = self.gate_docview.get_jpos_param().value()
            self.b_scan = self.hdf_doc.get_b_scan(None, col, dn0=dn_0, dn1=dn_1, fwf_arr=fwf_arr)

        self.bscan_changed_event(self.b_scan)

    # def set_orientation(self, changeDesc, orientation):
    #     self.set_bscan()

    def AddChildWithSlot(self, dict, slot):
        child = self.addChild(dict)
        child.sigValueChanged.connect(slot)

    def on_update_ij_pos(self, i_indx, j_indx):
        self.set_bscan()

    def on_update_time_range(self):
        self.set_bscan()

    def on_update_fwf(self):
        self.set_bscan()